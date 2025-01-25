package gotdf_python

/*
All public (upper-case) functions here should be available to Python.

As a result, all public functions should be imported & tested.

Currently, testing is performed via 'validate_otdf_python.py'

FIXME: Expand test coverage, with known good attributes.  See: https://github.com/orgs/opentdf/discussions/947

*/
import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path"
	"path/filepath"
	"strings"

	"github.com/opentdf/platform/sdk"
)

/*
A simple "Hello, world" function, used for learning golang (e.g. unit testing),
as well as validating the necessary mechanisms to compile this library
into a Python wheel.

In the future, this function might be removed or replaced with a more
conventional & useful function like GetVersion()
*/
func Hello() string {
	return "Hello, world"
}

type TokenAuth struct {
	AccessToken string
	NpeClientId string
}

type OpentdfConfig struct {
	ClientId         string
	ClientSecret     string
	PlatformEndpoint string
	TokenEndpoint    string
	KasUrl           string
}

/*
Based on: https://stackoverflow.com/a/42849112
func inputValidation(normalConfig DecryptionConfig) (*DecryptionConfig, error) {
	// Convert our Struct to a Map
	var inInterface map[string]interface{}
	inrec, _ := json.Marshal(normalConfig)
	json.Unmarshal(inrec, &inInterface)

	// Iterate through fields in the map and fail if empty value found
	for field, val := range inInterface {
		if val == nil || val == "" {
			// fmt.Println("KV Pair: ", field, val)
			return nil, errors.New("Missing configuration value for field " + field)
		}
	}

	return &normalConfig, nil
}
*/

func newSdkClient(config OpentdfConfig, authScopes []string) (*sdk.SDK, error) {
	// NOTE: The 'platformEndpoint' is sometimes referenced as 'host'
	if strings.Count(config.TokenEndpoint, "http://") == 1 {
		return sdk.New(config.PlatformEndpoint,
			sdk.WithClientCredentials(config.ClientId, config.ClientSecret, authScopes),
			sdk.WithTokenEndpoint(config.TokenEndpoint),
			sdk.WithInsecurePlaintextConn(),
		)
	} else if strings.Count(config.TokenEndpoint, "https://") == 1 {
		return sdk.New(config.PlatformEndpoint,
			sdk.WithClientCredentials(config.ClientId, config.ClientSecret, authScopes),
			sdk.WithTokenEndpoint(config.TokenEndpoint),
			sdk.WithInsecureSkipVerifyConn(),
		)
	} else {
		return nil, errors.New("invalid TokenEndpoint given")
	}
}

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
		return sdk.New(config.PlatformEndpoint,
			sdk.WithClientCredentials(config.ClientId, config.ClientSecret, authScopes),
			sdk.WithTokenEndpoint(config.TokenEndpoint),
			sdk.WithTokenExchange(token.AccessToken, []string{token.NpeClientId}),
			sdk.WithInsecureSkipVerifyConn(),
		)
	} else {
		return nil, errors.New("invalid TokenEndpoint given")
	}
}

func EncryptString(inputText string, config OpentdfConfig, dataAttributes []string) (string, error) {
	strReader := strings.NewReader(inputText)

	// Scopes is related to OIDC, it's about what you're requesting
	// and access control from the IdP
	authScopes := []string{"email"}
	// var authScopes []string

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
func EncryptStringPE(inputText string, config OpentdfConfig, token TokenAuth, dataAttributes []string) (string, string, error) {
	// Scopes relate to OIDC, it's about what you're requesting
	// and access control from the IdP
	authScopes := []string{"email"}

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

func DecryptStringPE(inputText string, config OpentdfConfig, token TokenAuth) (string, error) {

	// Scopes relate to OIDC, it's about what you're requesting
	// and access control from the IdP
	authScopes := []string{"email"}

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

func EncryptFile(inputFilePath string, outputFilePath string, config OpentdfConfig, dataAttributes []string) (string, error) {
	authScopes := []string{"email"}

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
	EncryptFilesInDir encrypts all files in the specified directory

Work is performed as an NPE (Non-Person Entity). Encrypted files are placed
in the same directory as the input files, with a .tdf extension added to the file name.
*/
func EncryptFilesInDir(dirPath string, config OpentdfConfig, dataAttributes []string) ([]string, error) {
	files, err := ioutil.ReadDir(dirPath)
	if err != nil {
		return nil, err
	}

	var outputPaths []string
	for _, file := range files {
		if !file.IsDir() {
			inputFilePath := path.Join(dirPath, file.Name())
			outputFilePath := inputFilePath + ".tdf"
			got, err := EncryptFile(inputFilePath, outputFilePath, config, dataAttributes)
			if err != nil {
				log.Printf("Failed to encrypt file %s: %v", inputFilePath, err)
				return nil, err
			} else {
				outputPaths = append(outputPaths, got)
			}
		}
	}
	return outputPaths, nil
}

/*
	EncryptFilesGlob encrypts all files matching the specified glob pattern.

Work is performed as an NPE (Non-Person Entity). Encrypted files are placed
in the same directory as the input files, with a .tdf extension added to the file name.
*/
func EncryptFilesGlob(pattern string, config OpentdfConfig, dataAttributes []string) ([]string, error) {
	files, err := filepath.Glob(pattern)
	if err != nil {
		return nil, err
	}

	var outputPaths []string
	for _, inputFilePath := range files {
		outputFilePath := inputFilePath + ".tdf"
		got, err := EncryptFile(inputFilePath, outputFilePath, config, dataAttributes)
		if err != nil {
			log.Printf("Failed to encrypt file %s: %v", inputFilePath, err)
			return nil, err
		} else {
			outputPaths = append(outputPaths, got)
		}
	}
	return outputPaths, nil
}

/*
Encrypts a file as a PE (Person Entity), returning a TDF manifest and the cipher text.
*/
func EncryptFilePE(inputFilePath string, outputFilePath string, config OpentdfConfig, token TokenAuth, dataAttributes []string) (string, error) {
	authScopes := []string{"email"}

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
TODO: Create a single global var for sdkClinet (global var)
  - E.g. in an HTTP server, create an instance for each connection

TODO: The platform knows about the IdP, therefore we don't need
to specify the TOKEN_ENDPOINT.

TODO: Research why the platform is hard-coding "email" for scope

A non-Public decrypt function.

Based on:
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

func DecryptFilePE(inputFilePath string, outputFilePath string, config OpentdfConfig, token TokenAuth) (string, error) {
	bytes, err := readBytesFromFile(inputFilePath)
	if err != nil {
		return "", err
	}
	authScopes := []string{"email"}
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
