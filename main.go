package gotdf_python

/*
All public (upper-case) functions here should be available to Python.
* E.g. imported & tested via 'validate_otdf_python.py'

TODO: Consider testing against attributes that are returned by some listing.
* See: https://github.com/orgs/opentdf/discussions/947

TODO: Consider exposing an sdkClient that can be returned to the caller
* Note, previously this failed in a 'gopy' compiled context

*/
import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"os"
	"path"
	"path/filepath"
	"strings"
	"sync"

	"github.com/opentdf/platform/sdk"
)

type TokenAuth struct {
	AccessToken string
	NpeClientId string
}

type OpentdfConfig struct {
	ClientId           string
	ClientSecret       string
	PlatformEndpoint   string
	TokenEndpoint      string
	KasUrl             string
	InsecureSkipVerify bool
}

func getEnv(key, defaultValue string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return defaultValue
}

func newSdkClient(config OpentdfConfig, authScopes []string) (*sdk.SDK, error) {
	// NOTE: The 'platformEndpoint' is sometimes referenced as 'host'
	if strings.Count(config.TokenEndpoint, "http://") == 1 {
		return sdk.New(config.PlatformEndpoint,
			sdk.WithClientCredentials(config.ClientId, config.ClientSecret, authScopes),
			sdk.WithTokenEndpoint(config.TokenEndpoint),
			sdk.WithInsecurePlaintextConn(),
		)
	} else if strings.Count(config.TokenEndpoint, "https://") == 1 {
		opts := []sdk.Option{
			sdk.WithClientCredentials(config.ClientId, config.ClientSecret, authScopes),
			sdk.WithTokenEndpoint(config.TokenEndpoint),
		}

		if config.InsecureSkipVerify {
			opts = append(opts, sdk.WithInsecureSkipVerifyConn())
		}

		return sdk.New(config.PlatformEndpoint, opts...)
	} else {
		return nil, errors.New("invalid TokenEndpoint given")
	}
}

/*
NOTE: When the environment variable 'INSECURE_SKIP_VERIFY' is set to 'TRUE',
this option for the OpenTDF SDK will be set.
*/
func peSdkClient(config OpentdfConfig, authScopes []string, token TokenAuth) (*sdk.SDK, error) {
	// NOTE: The 'platformEndpoint' is sometimes referenced as 'host'
	if strings.Count(config.TokenEndpoint, "http://") == 1 {
		return sdk.New(config.PlatformEndpoint,
			sdk.WithClientCredentials(config.ClientId, config.ClientSecret, authScopes),
			sdk.WithTokenEndpoint(config.TokenEndpoint),
			sdk.WithTokenExchange(token.AccessToken, []string{token.NpeClientId}),
			sdk.WithInsecurePlaintextConn(),
		)
	} else if strings.Count(config.TokenEndpoint, "https://") == 1 {
		opts := []sdk.Option{
			sdk.WithClientCredentials(config.ClientId, config.ClientSecret, authScopes),
			sdk.WithTokenEndpoint(config.TokenEndpoint),
			sdk.WithTokenExchange(token.AccessToken, []string{token.NpeClientId}),
		}

		if config.InsecureSkipVerify {
			opts = append(opts, sdk.WithInsecureSkipVerifyConn())
		}

		return sdk.New(config.PlatformEndpoint, opts...)
	} else {
		return nil, errors.New("invalid TokenEndpoint given")
	}
}

func EncryptString(inputText string, config OpentdfConfig, dataAttributes []string, authScopes []string) (string, error) {
	strReader := strings.NewReader(inputText)
	sdkClient, err := newSdkClient(config, authScopes)

	if err != nil {
		return "", err
	}

	tdfFile, err := os.Create("sensitive.txt.tdf")
	if err != nil {
		return "", err
	}
	defer tdfFile.Close()

	if strings.Count(config.KasUrl, "http") != 1 {
		return "", errors.New("invalid KAS Url, should contain single protocol")
	}

	tdf, err := sdkClient.CreateTDF(
		tdfFile,
		strReader,
		// sdk.WithDataAttributes("https://example.com/attributes/1", "https://example.com/attributes/2"),
		// sdk.WithDataAttributes("https://example.com/attr/attr1/value/value1"),
		sdk.WithDataAttributes(dataAttributes...),
		sdk.WithKasInformation(
			sdk.KASInfo{
				// examples assume insecure http
				URL:       config.KasUrl,
				PublicKey: "",
			}),
	)

	if err != nil {
		return "", err
	}

	manifestJSON, err := json.MarshalIndent(tdf.Manifest(), "", "  ")
	if err != nil {
		return "", err
	}

	// IF DEBUG: ... Print Manifest
	// fmt.Println(string(manifestJSON))
	return string(manifestJSON), nil
}

/*
Encrypts a string as a PE (Person Entity), returning a TDF manifest and the cipher text.
*/
func EncryptStringPE(inputText string, config OpentdfConfig, token TokenAuth, dataAttributes []string, authScopes []string) (string, string, error) {
	sdkClient, err := peSdkClient(config, authScopes, token)

	if err != nil {
		return "", "", err
	}

	// tdfFile, err := os.Create("sensitive.txt.tdf")
	// if err != nil {
	// 	return "", err
	// }
	// defer tdfFile.Close()

	if strings.Count(config.KasUrl, "http") != 1 {
		return "", "", errors.New("invalid KAS Url, should contain single protocol")
	}

	plaintext := strings.NewReader(inputText)
	ciphertext := new(bytes.Buffer)

	tdf, err := sdkClient.CreateTDF(
		// tdfFile,
		ciphertext,
		plaintext,
		sdk.WithDataAttributes(dataAttributes...),
		sdk.WithKasInformation(
			sdk.KASInfo{
				// examples assume insecure http
				URL:       config.KasUrl,
				PublicKey: "",
			}),
	)

	if err != nil {
		return "", "", err
	}

	manifestJSON, err := json.MarshalIndent(tdf.Manifest(), "", "  ")
	if err != nil {
		return "", "", err
	}

	// Print Manifest (maybe useful in debugging)
	// fmt.Println(string(manifestJSON))
	return string(manifestJSON), ciphertext.String(), nil
}

func DecryptStringPE(inputText string, config OpentdfConfig, token TokenAuth, authScopes []string) (string, error) {
	decrypted, err := decryptBytesPE([]byte(inputText), authScopes, config, token)
	if err != nil {
		return "", err
	}

	return decrypted.String(), nil
}

func readBytesFromFile(filePath string) ([]byte, error) {
	if filePath == "" {
		return nil, errors.New("invalid input file path given")
	}
	fileToEncrypt, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open file at path: %s", filePath)
	}
	defer fileToEncrypt.Close()

	bytes, err := io.ReadAll(fileToEncrypt)
	if err != nil {
		return nil, fmt.Errorf("failed to read bytes from file at path: %s", filePath)
	}
	return bytes, err
}

/*
The encryptBytesNPE function below is based on the 'EncryptBytes()' function
provided by otdfctl.

NOTE: the original 'EncryptBytes()' function has a parameter named
'scopes', we've changed that variable name to 'authScopes' for more
clarity.

One noticeable difference is that rather than having state kept
in the CLI, we provide our own input parameter OpentdfConfig.

See:

	https://github.com/opentdf/otdfctl/blob/46cfca1ba32c57f7264c320db27394c00412ca49/pkg/handlers/tdf.go#L10-L27
*/
func encryptBytesNPE(b []byte, authScopes []string, config OpentdfConfig, dataAttributes []string) (*bytes.Buffer, error) {
	sdkClient, err := newSdkClient(config, authScopes)

	if err != nil {
		return nil, err
	}

	var encrypted []byte
	enc := bytes.NewBuffer(encrypted)

	// TODO: validate values are FQNs or return an error [https://github.com/opentdf/platform/issues/515]
	_, err = sdkClient.CreateTDF(enc, bytes.NewReader(b),
		sdk.WithDataAttributes(dataAttributes...),
		sdk.WithKasInformation(sdk.KASInfo{
			URL:       config.KasUrl,
			PublicKey: "",
		},
		),
	)
	if err != nil {
		return nil, err
	}
	return enc, nil
}

func encryptBytesPE(b []byte, authScopes []string, config OpentdfConfig, token TokenAuth, dataAttributes []string) (*bytes.Buffer, error) {
	sdkClient, err := peSdkClient(config, authScopes, token)

	if err != nil {
		return nil, err
	}

	var encrypted []byte
	enc := bytes.NewBuffer(encrypted)

	// TODO: validate values are FQNs or return an error [https://github.com/opentdf/platform/issues/515]
	_, err = sdkClient.CreateTDF(enc, bytes.NewReader(b),
		sdk.WithDataAttributes(dataAttributes...),
		sdk.WithKasInformation(sdk.KASInfo{
			URL:       config.KasUrl,
			PublicKey: "",
		},
		),
	)
	if err != nil {
		return nil, err
	}
	return enc, nil
}

func EncryptFile(inputFilePath string, outputFilePath string, config OpentdfConfig, dataAttributes []string, authScopes []string) (string, error) {
	if outputFilePath == "" {
		return "", errors.New("invalid output file path given")
	}

	bytes, err := readBytesFromFile(inputFilePath)

	if err != nil {
		return "", err
	}

	// If necessary, bytes can be printed for debugging
	// fmt.Print(bytes)

	// Do the encryption
	encrypted, err := encryptBytesNPE(bytes, authScopes, config, dataAttributes)
	if err != nil {
		return "", fmt.Errorf("failed to encrypt: %w", err)
	}

	// Find the destination as the output flag filename or stdout
	var dest *os.File

	// make sure output ends in .tdf extension
	if !strings.HasSuffix(outputFilePath, ".tdf") {
		outputFilePath += ".tdf"
	}
	tdfFile, err := os.Create(outputFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to write encrypted file %s", outputFilePath)
	}
	defer tdfFile.Close()
	dest = tdfFile

	_, e := io.Copy(dest, encrypted)
	if e != nil {
		return "", errors.New("failed to write encrypted data to destination")
	}

	return outputFilePath, nil
}

/*
	EncryptFilesInDirNPE encrypts all files in the specified directory

Work is performed as an NPE (Non-Person Entity). Encrypted files are placed
in the same directory as the input files, with a .tdf extension added to the file name.
*/
func EncryptFilesInDirNPE(dirPath string, config OpentdfConfig, dataAttributes []string, authScopes []string) ([]string, error) {
	files, err := os.ReadDir(dirPath)
	if err != nil {
		return nil, err
	}
	errChan := make(chan error, len(files))

	var outputPaths []string
	var mu sync.Mutex
	var wg sync.WaitGroup

	for _, file := range files {
		if !file.IsDir() {
			wg.Add(1)
			go func(file os.DirEntry) {
				defer wg.Done()
				sdkClient, err := newSdkClient(config, authScopes)
				if err != nil {
					errChan <- fmt.Errorf("failed to create SDK client: %v", err)
					return
				}
				inputFilePath := path.Join(dirPath, file.Name())
				outputFilePath := inputFilePath + ".tdf"
				got, err := encryptFileWithClient(inputFilePath, outputFilePath, sdkClient, config, dataAttributes)
				if err != nil {
					errChan <- fmt.Errorf("failed to encrypt file %s: %v", inputFilePath, err)
					return
				}
				mu.Lock()
				outputPaths = append(outputPaths, got)
				mu.Unlock()
			}(file)
		}
	}

	wg.Wait()
	close(errChan)

	var errors []error
	for err := range errChan {
		errors = append(errors, err)
	}

	logOutputPaths(outputPaths, errors)

	if len(errors) > 0 {
		return outputPaths, fmt.Errorf("encountered errors during encryption: %v", errors)
	}
	return outputPaths, nil
}

/*
	EncryptFilesWithExtensionsNPE encrypts all files in 'dirPath' with given file 'extensions'.

Work is performed as an NPE (Non-Person Entity). Encrypted files are placed
in the same directory as the input files, with a .tdf extension added to the file name.
*/
func EncryptFilesWithExtensionsNPE(dirPath string, extensions []string, config OpentdfConfig, dataAttributes []string, authScopes []string) ([]string, error) {
	sdkClient, err := newSdkClient(config, authScopes)
	if err != nil {
		return nil, err
	}

	files, err := findFiles(dirPath, extensions)
	if err != nil {
		return nil, err
	}

	var outputPaths = make([]string, 0, len(files))
	var errors = make([]error, 0, len(files))
	for _, file := range files {
		inputFilePath := file
		outputFilePath := inputFilePath + ".tdf"
		got, err := encryptFileWithClient(inputFilePath, outputFilePath, sdkClient, config, dataAttributes)
		if err != nil {
			errors = append(errors, fmt.Errorf("failed to encrypt file %s: %v", inputFilePath, err))
			continue
		}
		outputPaths = append(outputPaths, got)
	}

	logOutputPaths(outputPaths, errors)

	if len(errors) > 0 {
		return outputPaths, fmt.Errorf("encountered errors during encryption: %v", errors)
	}
	return outputPaths, nil
}

/*
Encrypts a file as a PE (Person Entity), returning a TDF manifest and the cipher text.
*/
func EncryptFilePE(inputFilePath string, outputFilePath string, config OpentdfConfig, token TokenAuth, dataAttributes []string, authScopes []string) (string, error) {
	if outputFilePath == "" {
		return "", errors.New("invalid output file path given")
	}

	bytes, err := readBytesFromFile(inputFilePath)

	if err != nil {
		return "", err
	}

	// If necessary, bytes can be printed for debugging
	// fmt.Print(bytes)

	// Do the encryption
	encrypted, err := encryptBytesPE(bytes, authScopes, config, token, dataAttributes)
	if err != nil {
		return "", fmt.Errorf("failed to encrypt: %w", err)
	}

	// Find the destination as the output flag filename or stdout
	var dest *os.File

	// make sure output ends in .tdf extension
	if !strings.HasSuffix(outputFilePath, ".tdf") {
		return "", fmt.Errorf("output file path '%s' should have .tdf extension", outputFilePath)
	}
	tdfFile, err := os.Create(outputFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to write encrypted file %s", outputFilePath)
	}
	defer tdfFile.Close()
	dest = tdfFile

	_, e := io.Copy(dest, encrypted)
	if e != nil {
		return "", errors.New("failed to write encrypted data to destination")
	}

	return outputFilePath, nil
}

/*
A non-Public decrypt function, based on:
- https://github.com/opentdf/otdfctl/blob/46cfca1ba32c57f7264c320db27394c00412ca49/pkg/handlers/tdf.go#L29-L41
*/
func decryptBytes(toDecrypt []byte, authScopes []string, config OpentdfConfig) (*bytes.Buffer, error) {
	sdkClient, err := newSdkClient(config, authScopes)

	if err != nil {
		return nil, err
	}

	tdfreader, err := sdkClient.LoadTDF(bytes.NewReader(toDecrypt))
	if err != nil {
		return nil, err
	}

	buf := new(bytes.Buffer)
	_, err = io.Copy(buf, tdfreader)
	if err != nil && err != io.EOF {
		return nil, err
	}
	return buf, nil
}

func decryptBytesPE(toDecrypt []byte, authScopes []string, config OpentdfConfig, token TokenAuth) (*bytes.Buffer, error) {

	sdkClient, err := peSdkClient(config, authScopes, token)

	if err != nil {
		return nil, err
	}

	reader, err := sdkClient.LoadTDF(bytes.NewReader(toDecrypt))
	if err != nil {
		return nil, err
	}

	buf := new(bytes.Buffer)
	_, err = io.Copy(buf, reader)
	if err != nil && err != io.EOF {
		return nil, err
	}
	return buf, nil
}

func DecryptFile(inputFilePath string, outputFilePath string, config OpentdfConfig) (string, error) {
	bytes, err := readBytesFromFile(inputFilePath)
	if err != nil {
		return "", err
	}

	decrypted, err := decryptBytes(bytes, nil, config)
	if err != nil {
		return "", err
	}

	tdfFile, err := os.Create(outputFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to write decrypted file %s", outputFilePath)
	}
	defer tdfFile.Close()

	_, e := io.Copy(tdfFile, decrypted)
	if e != nil {
		return "", errors.New("failed to write decrypted data to destination")
	}

	return outputFilePath, nil
}

/*
DecryptFilesInDirNPE decrypts all files in the specified directory
Work is performed as an NPE (Non-Person Entity). Decrypted files are placed
in the same directory as the input files, with the .tdf extension removed from the file name.
*/
func DecryptFilesInDirNPE(dirPath string, config OpentdfConfig, authScopes []string) ([]string, error) {
	files, err := os.ReadDir(dirPath)
	if err != nil {
		return nil, err
	}

	var wg sync.WaitGroup
	outputPathsChan := make(chan string, len(files))
	errChan := make(chan error, len(files))

	for _, file := range files {
		if !file.IsDir() && strings.HasSuffix(file.Name(), ".tdf") {
			wg.Add(1)
			go func(file os.DirEntry) {
				defer wg.Done()
				sdkClient, err := newSdkClient(config, authScopes)
				if err != nil {
					errChan <- fmt.Errorf("failed to create SDK client: %v", err)
					return
				}

				fileInfo, err := file.Info()
				if err != nil {
					errChan <- fmt.Errorf("failed to get file info for %s: %v", file.Name(), err)
					return
				}
				inputFilePath := path.Join(dirPath, fileInfo.Name())
				outputFilePath := strings.TrimSuffix(inputFilePath, ".tdf")

				bytes, err := readBytesFromFile(inputFilePath)
				if err != nil {
					errChan <- fmt.Errorf("failed to read file %s: %v", inputFilePath, err)
					return
				}

				decrypted, err := decryptBytesWithClient(bytes, sdkClient)
				if err != nil {
					errChan <- fmt.Errorf("failed to decrypt file %s: %v", inputFilePath, err)
					return
				}

				tdfFile, err := os.Create(outputFilePath)
				if err != nil {
					errChan <- fmt.Errorf("failed to write decrypted file %s: %v", outputFilePath, err)
					return
				}
				defer tdfFile.Close()

				_, e := io.Copy(tdfFile, decrypted)
				if e != nil {
					errChan <- fmt.Errorf("failed to write decrypted data to destination %s: %v", outputFilePath, err)
					return
				}

				outputPathsChan <- outputFilePath
			}(file)
		}
	}

	wg.Wait()
	close(outputPathsChan)
	close(errChan)

	var outputPaths []string
	for path := range outputPathsChan {
		outputPaths = append(outputPaths, path)
	}

	var errors []error
	for err := range errChan {
		errors = append(errors, err)
	}

	logOutputPaths(outputPaths, errors)

	if len(errors) > 0 {
		return nil, fmt.Errorf("encountered errors during decryption: %v", errors)
	}

	return outputPaths, nil
}

/*
DecryptFilesWithExtensionsNPE decrypts all files matching the file 'extensions' in 'dirPath'.
Work is performed as an NPE (Non-Person Entity). Decrypted files are placed
in the same directory as the input files, with the .tdf extension removed from the file name.
*/
func DecryptFilesWithExtensionsNPE(dirPath string, extensions []string, config OpentdfConfig, authScopes []string) ([]string, error) {
	files, err := os.ReadDir(dirPath)
	if err != nil {
		return nil, err
	}

	outputPathsChan := make(chan string, len(files))
	errChan := make(chan error, len(files))

	var wg sync.WaitGroup

	for _, file := range files {
		if !file.IsDir() {
			for _, ext := range extensions {
				if strings.HasSuffix(file.Name(), ext) {
					wg.Add(1)
					go func(file os.DirEntry, ext string) {
						defer wg.Done()
						sdkClient, err := newSdkClient(config, authScopes)
						if err != nil {
							errChan <- fmt.Errorf("failed to create SDK client: %v", err)
							return
						}

						inputFilePath := filepath.Join(dirPath, file.Name())
						outputFilePath := strings.TrimSuffix(inputFilePath, ext)

						bytes, err := readBytesFromFile(inputFilePath)
						if err != nil {
							errChan <- fmt.Errorf("failed to read file %s: %v", inputFilePath, err)
							return
						}

						decrypted, err := decryptBytesWithClient(bytes, sdkClient)
						if err != nil {
							errChan <- fmt.Errorf("failed to decrypt file %s: %v", inputFilePath, err)
							return
						}

						tdfFile, err := os.Create(outputFilePath)
						if err != nil {
							errChan <- fmt.Errorf("failed to write decrypted file %s: %v", outputFilePath, err)
							return
						}
						defer tdfFile.Close()

						_, e := io.Copy(tdfFile, decrypted)
						if e != nil {
							errChan <- fmt.Errorf("failed to write decrypted data to destination %s: %v", outputFilePath, err)
							return
						}

						outputPathsChan <- outputFilePath
					}(file, ext)
				}
			}
		}
	}

	wg.Wait()
	close(outputPathsChan)
	close(errChan)

	var outputPaths []string
	for path := range outputPathsChan {
		outputPaths = append(outputPaths, path)
	}

	var errors []error
	for err := range errChan {
		errors = append(errors, err)
	}

	logOutputPaths(outputPaths, errors)

	if len(outputPaths) == 0 {
		if len(errors) == 0 {
			return nil, fmt.Errorf("no files with extensions %v found in directory %s", extensions, dirPath)
		}
		return nil, fmt.Errorf("encountered errors during decryption of files in directory %s: %v", dirPath, errors)
	}
	return outputPaths, nil
}

func decryptBytesWithClient(toDecrypt []byte, sdkClient *sdk.SDK) (*bytes.Buffer, error) {
	tdfreader, err := sdkClient.LoadTDF(bytes.NewReader(toDecrypt))
	if err != nil {
		return nil, err
	}

	buf := new(bytes.Buffer)
	_, err = io.Copy(buf, tdfreader)
	if err != nil && err != io.EOF {
		return nil, err
	}
	return buf, nil
}

func DecryptFilePE(inputFilePath string, outputFilePath string, config OpentdfConfig, token TokenAuth, authScopes []string) (string, error) {
	bytes, err := readBytesFromFile(inputFilePath)
	if err != nil {
		return "", err
	}
	decrypted, err := decryptBytesPE(bytes, authScopes, config, token)
	if err != nil {
		return "", err
	}

	tdfFile, err := os.Create(outputFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to write decrypted file %s", outputFilePath)
	}
	defer tdfFile.Close()

	_, e := io.Copy(tdfFile, decrypted)
	if e != nil {
		return "", errors.New("failed to write decrypted data to destination")
	}

	return outputFilePath, nil
}

func encryptFileWithClient(inputFilePath string, outputFilePath string, sdkClient *sdk.SDK, config OpentdfConfig, dataAttributes []string) (string, error) {
	bytes, err := readBytesFromFile(inputFilePath)
	if err != nil {
		return "", err
	}

	encrypted, err := encryptBytesWithClient(bytes, sdkClient, config, dataAttributes)
	if err != nil {
		return "", fmt.Errorf("failed to encrypt: %w", err)
	}

	var dest *os.File
	if !strings.HasSuffix(outputFilePath, ".tdf") {
		outputFilePath += ".tdf"
	}
	tdfFile, err := os.Create(outputFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to write encrypted file %s", outputFilePath)
	}
	defer tdfFile.Close()
	dest = tdfFile

	_, e := io.Copy(dest, encrypted)
	if e != nil {
		return "", errors.New("failed to write encrypted data to destination")
	}

	return outputFilePath, nil
}

func encryptBytesWithClient(b []byte, sdkClient *sdk.SDK, config OpentdfConfig, dataAttributes []string) (*bytes.Buffer, error) {
	var encrypted []byte
	enc := bytes.NewBuffer(encrypted)

	_, err := sdkClient.CreateTDF(enc, bytes.NewReader(b),
		sdk.WithDataAttributes(dataAttributes...),
		sdk.WithKasInformation(sdk.KASInfo{
			URL:       config.KasUrl,
			PublicKey: "",
		}),
	)
	if err != nil {
		return nil, err
	}
	return enc, nil
}

// Function to find all files recursively in a directory matching the given extensions
func findFiles(dir string, extensions []string) ([]string, error) {
	var files []string

	// Use filepath.Walk to walk through the directory recursively
	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			// If there's an error reading the file, skip it
			return err
		}

		// Check if the file extension matches 'extensions' parameter
		if !info.IsDir() && strings.Contains(strings.Join(extensions, ","), filepath.Ext(path)) {
			files = append(files, path) // Add the file to the list
		}

		return nil
	})

	if err != nil {
		return nil, err
	}

	return files, nil
}

// logOutputPaths logs the output paths and any errors that occurred during processing
func logOutputPaths(outputPaths []string, errors []error) {
	if len(errors) > 0 {
		log.Println("Errors occurred during processing:")
		for _, err := range errors {
			log.Printf("\t%s\n", err)
		}
	}
	log.Println("Output Paths:")
	for _, path := range outputPaths {
		log.Printf("\t%s\n", path)
	}
}
