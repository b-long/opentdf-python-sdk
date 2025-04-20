package gotdf_python_test

import (
	"crypto/tls"
	"encoding/json"
	"errors"
	"fmt"
	"gotdf_python"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"testing"
	"time"
)

var defaultAuthScopes = []string{"email"}

func getEnv(key, defaultValue string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return defaultValue
}

type TestConfiguration struct {
	platformEndpoint string
	tokenEndpoint    string
	kasEndpoint      string
	npeClientId      string
	npeClientSecret  string
	peUsername       string
	pePassword       string
	testAttribute1   string
	testAttribute2   string
}

var config = TestConfiguration{
	platformEndpoint: os.Getenv("OPENTDF_HOSTNAME"),
	tokenEndpoint:    os.Getenv("OIDC_TOKEN_ENDPOINT"),
	kasEndpoint:      os.Getenv("OPENTDF_KAS_URL"),
	npeClientId:      os.Getenv("OPENTDF_CLIENT_ID"),
	npeClientSecret:  os.Getenv("OPENTDF_CLIENT_SECRET"),
	peUsername:       os.Getenv("TEST_OPENTDF_SECRET_USER_ID"),
	pePassword:       os.Getenv("TEST_OPENTDF_SECRET_USER_PASSWORD"),
	// For default values, we added a helper function
	testAttribute1: getEnv("TEST_OPENTDF_ATTRIBUTE_1", "https://example.com/attr/attr1/value/value1"),
	testAttribute2: getEnv("TEST_OPENTDF_ATTRIBUTE_2", "https://example.com/attr/attr1/value/value2"),
}

/*
Parse a JSON string into a map

Based on: https://stackoverflow.com/a/72873915
*/
func jsonToMap(jsonStr string) map[string]interface{} {
	result := make(map[string]interface{})
	json.Unmarshal([]byte(jsonStr), &result)
	return result
}

/*
A basic HTTP request

Based on:
https://stackoverflow.com/q/24493116
*/
func authHelper(form url.Values, isPEAuth bool) (gotdf_python.TokenAuth, error) {
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	// FIXME: Use a client with TLS verification
	// client := http.Client{}
	client := &http.Client{Transport: tr}

	resp, err := client.PostForm(config.tokenEndpoint, form)

	//okay, moving on...
	if err != nil {
		log.Fatal(`Server`+config.tokenEndpoint+` returned an error.`, err)
	}

	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)

	if err != nil {
		log.Fatal(`Unable to read server response body`, err)
	}

	jsonMap := jsonToMap(string(body))

	val, ok := jsonMap["access_token"].(string)
	// If the key exists
	if !ok {
		return gotdf_python.TokenAuth{}, errors.New("Unable to obtain 'access_token', cannot continue")
	}

	if isPEAuth {
		fmt.Println("Successfully auth'd PE", config.peUsername)

		return gotdf_python.TokenAuth{
			AccessToken: val,
			NpeClientId: config.npeClientId,
		}, nil
	} else {
		fmt.Println("Successfully auth'd NPE", config.npeClientId)

		return gotdf_python.TokenAuth{
			AccessToken: val,
		}, nil
	}
}

func AuthenticatePE() (gotdf_python.TokenAuth, error) {
	form := url.Values{}
	form.Add("grant_type", "password")
	form.Add("client_id", config.npeClientId)
	form.Add("client_secret", config.npeClientSecret)
	form.Add("username", config.peUsername)
	form.Add("password", config.pePassword)
	return authHelper(form, true)
}

func AuthenticateNPE() (gotdf_python.TokenAuth, error) {
	form := url.Values{}
	form.Add("grant_type", "client_credentials")
	form.Add("client_id", config.npeClientId)
	form.Add("client_secret", config.npeClientSecret)
	return authHelper(form, false)
}

func getSingleDataAttribute(config TestConfiguration) []string {
	return []string{config.testAttribute1}
}
func getMultiDataAttribute(config TestConfiguration) []string {
	return []string{config.testAttribute1, config.testAttribute2}
}

func doEncryptString(t *testing.T, dataAttributes []string) {

	got, err := gotdf_python.EncryptString("Hello, world", gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, dataAttributes, defaultAuthScopes)
	if err != nil {
		t.Fatal(err)
	}

	if got == "" {
		t.Fatal("EncryptString returned empty value, but didn't error!")
	} else {
		if len(got) < 1000 {
			// NOTE: Testing the size of the stringified JSON is not
			// necessarily a good test.  However, it is one way to ensure
			// that we received something AND that the thing is
			// JSON-seriazable
			t.Error("Unexpected value")
		}
		fmt.Println("Got a TDF manifest")
	}
}

func Test_NPE_Encrypt_String_Nil_Attributes(t *testing.T) {
	doEncryptString(t, nil)
}

func Test_NPE_Encrypt_String_Single_Attributes(t *testing.T) {
	attrValues := getSingleDataAttribute(config)
	doEncryptString(t, attrValues)

}

func Test_NPE_Encrypt_String_Multiple_Attributes(t *testing.T) {
	attrValues := getMultiDataAttribute(config)

	doEncryptString(t, attrValues)

}

func encrypt_file_NPE(t *testing.T, dataAttributes []string) string {
	tmpInputFile, err := os.CreateTemp(t.TempDir(), "input-file.txt")
	if err != nil {
		log.Fatal("Could not create input file", err)
	}
	defer tmpInputFile.Close()

	fmt.Println("Created input file: ", tmpInputFile.Name())

	fmt.Println("Writing some data to the input file")
	if _, err = tmpInputFile.WriteString("test data"); err != nil {
		log.Fatal("Unable to write to temporary file", err)
	} else {
		fmt.Println("Data should have been written")
	}

	tmpOutputFile, err := os.CreateTemp("", "output-file-*.txt")

	if err != nil {
		log.Fatal("Could not create output file", err)
	}
	defer tmpOutputFile.Close()

	got, err := gotdf_python.EncryptFile(tmpInputFile.Name(), tmpOutputFile.Name(), gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, dataAttributes, defaultAuthScopes)
	if err != nil {
		t.Error("Failed to EncryptFile()!")
	}

	if got == "" {
		t.Error("Unexpected value")
	}

	if !strings.HasSuffix(got, ".tdf") {
		t.Error("All output files should have the .tdf extension")
	}

	fmt.Println("Got a TDF manifest")
	return got
}

func encrypt_file_PE(t *testing.T, dataAttributes []string, tokenAuth gotdf_python.TokenAuth) string {
	tmpInputFile, err := os.CreateTemp("", "input-file-*.txt")
	if err != nil {
		log.Fatal("Could not create input file", err)
	}
	defer tmpInputFile.Close()

	fmt.Println("Created input file: ", tmpInputFile.Name())

	fmt.Println("Writing some data to the input file")
	if _, err = tmpInputFile.WriteString("PE test data"); err != nil {
		log.Fatal("Unable to write to temporary file", err)
	} else {
		fmt.Println("Data should have been written")
	}

	tmpOutputFile, err := os.CreateTemp("", "*.tdf")

	if err != nil {
		log.Fatal("Could not create output file", err)
	}
	defer tmpOutputFile.Close()

	got, err := gotdf_python.EncryptFilePE(tmpInputFile.Name(), tmpOutputFile.Name(), gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, tokenAuth, dataAttributes, defaultAuthScopes)
	if err != nil {
		t.Fatal("Failed to EncryptFilePE()!")
	}

	if got == "" {
		t.Fatal("Unexpected value")
	}

	if !strings.HasSuffix(got, ".tdf") {
		t.Fatal("All output files should have the .tdf extension")
	}

	fmt.Println("TDF file written to disk")
	return got
}

func Test_NPE_Encrypt_File_Nil_Attributes(t *testing.T) {
	encrypt_file_NPE(t, nil)
}

func Test_NPE_Encrypt_File_Single_Attributes(t *testing.T) {
	attrValues := getSingleDataAttribute(config)
	encrypt_file_NPE(t, attrValues)
}

func Test_NPE_Encrypt_File_Multi_Attributes(t *testing.T) {
	attrValues := getMultiDataAttribute(config)

	encrypt_file_NPE(t, attrValues)
}

func e2e_test_as_PE(t *testing.T, dataAttributes []string) {
	token_for_encrypt, err := AuthenticatePE()
	if err != nil {
		t.Error(err)
	}

	input_TDF_path := encrypt_file_PE(t, dataAttributes, token_for_encrypt)

	time.Sleep(4000 * time.Millisecond)

	plaintext_output_path, err := os.CreateTemp("", "output-file-*.txt")
	if err != nil {
		t.Fatal(err)
	}

	token_for_decrypt, err := AuthenticatePE()
	if err != nil {
		t.Error(err)
	}
	got, err := gotdf_python.DecryptFilePE(input_TDF_path, plaintext_output_path.Name(), gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, token_for_decrypt, defaultAuthScopes)
	if err != nil {
		t.Fatal(err)
	}
	if got == "" {
		t.Error("Unexpected value")
	} else {
		fmt.Println("Successfully decrypted TDF")
	}
}

func Test_PE_E2E_File_Nil_Attributes(t *testing.T) {
	e2e_test_as_PE(t, nil)
}

func Test_PE_E2E_File_Single_Attributes(t *testing.T) {
	attrValues := getSingleDataAttribute(config)
	e2e_test_as_PE(t, attrValues)
}

func Test_PE_E2E_File_Multi_Attributes(t *testing.T) {
	attrValues := getMultiDataAttribute(config)
	e2e_test_as_PE(t, attrValues)
}

func Test_Multifile_NPE_Encrypt_Files_In_Dir_Nil_Attributes(t *testing.T) {
	// Create a temporary directory
	tmpDir, err := os.MkdirTemp("", "input-dir")
	if err != nil {
		t.Fatal("Could not create temporary directory", err)
	}
	defer os.RemoveAll(tmpDir)

	// Create a temporary file in the directory
	tmpFile1, err := os.CreateTemp(tmpDir, "input-file1-*.txt")
	if err != nil {
		t.Fatal("Could not create input file", err)
	}
	defer tmpFile1.Close()

	// Write some data to the file
	if _, err = tmpFile1.WriteString("test data"); err != nil {
		t.Fatal("Unable to write to temporary file", err)
	}

	// Create a temporary file in the directory
	tmpFile2, err := os.CreateTemp(tmpDir, "input-file2-*.txt")
	if err != nil {
		t.Fatal("Could not create input file", err)
	}
	defer tmpFile2.Close()

	// Write some data to the file
	if _, err = tmpFile2.WriteString("test data"); err != nil {
		t.Fatal("Unable to write to temporary file", err)
	}

	// Create a temporary file in the directory
	tmpFile3, err := os.CreateTemp(tmpDir, "input-file3-*.csv")
	if err != nil {
		t.Fatal("Could not create input file", err)
	}
	defer tmpFile3.Close()

	// Write some data to the file
	if _, err = tmpFile3.WriteString("test data"); err != nil {
		t.Fatal("Unable to write to temporary file", err)
	}

	cfg := gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}

	got, err := gotdf_python.EncryptFilesWithExtensionsNPE(tmpDir, []string{".txt", ".csv"}, cfg, nil, defaultAuthScopes)
	if err != nil {
		t.Fatal("Failed to EncryptFilesWithExtensionsNPE()!", err)
	}

	if len(got) != 3 {
		t.Fatal("EncryptFilesWithExtensionsNPE returned incorrect got value, but didn't error!")
	}

	fmt.Println("Successfully encrypted files using file extensions")
}

// A new test of a new 'EncryptFilesWithExtensions' function
func Test_Multifile_NPE_Encrypt_Files_With_Extensions_Nil_Attributes(t *testing.T) {
	// Create a temporary directory
	tmpDir, err := os.MkdirTemp("", "input-dir")
	if err != nil {
		t.Fatal("Could not create temporary directory", err)
	}
	defer os.RemoveAll(tmpDir)

	// Create test files
	numFiles := createTestFiles(t, tmpDir)

	// Call the EncryptFilesWithExtensionsNPE function
	got, err := gotdf_python.EncryptFilesWithExtensionsNPE(tmpDir, []string{".txt", ".csv", ".pdf"}, gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, nil, defaultAuthScopes)
	if err != nil {
		t.Fatal("Failed to EncryptFilesWithExtensionsNPE()!", err)
	}

	if len(got) != numFiles {
		t.Fatal("EncryptFilesWithExtensionsNPE returned incorrect got value, but didn't error!")
	}

	fmt.Println("Successfully encrypted files with extensions")
}

// Call the DecryptFilesInDirNPE function
func Test_Multifile_NPE_Decrypt_Files_In_Dir_Nil_Attributes(t *testing.T) {
	// Create a temporary directory
	tmpDir, err := os.MkdirTemp("", "input-dir")
	if err != nil {
		t.Fatal("Could not create temporary directory", err)
	}
	defer os.RemoveAll(tmpDir)

	// Create test files
	numFiles := createTestFiles(t, tmpDir)

	// Encrypt the file
	_, err = gotdf_python.EncryptFilesInDirNPE(tmpDir, gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, nil, defaultAuthScopes)
	if err != nil {
		t.Fatal("Failed to EncryptFilesInDirNPE()!", err)
	}

	// Call the DecryptFilesInDirNPE function
	got, err := gotdf_python.DecryptFilesInDirNPE(tmpDir, gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, defaultAuthScopes)
	if err != nil {
		t.Fatal("Failed to DecryptFilesInDirNPE()!", err)
	}

	if len(got) != numFiles {
		t.Fatal("DecryptFilesInDirNPE returned empty value, but didn't error!")
	}

	fmt.Println("Successfully decrypted files in directory")
}

func Test_Multifile_NPE_Decrypt_Files_With_Extensions_Nil_Attributes(t *testing.T) {
	// Create a temporary directory
	tmpDir, err := os.MkdirTemp("", "input-dir")
	if err != nil {
		t.Fatal("Could not create temporary directory", err)
	}
	defer os.RemoveAll(tmpDir)

	// Create test files
	numFiles := createTestFiles(t, tmpDir)

	// Encrypt the files
	_, err = gotdf_python.EncryptFilesWithExtensionsNPE(tmpDir, []string{".txt", ".csv", ".pdf"}, gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, nil, defaultAuthScopes)
	if err != nil {
		t.Fatal("Failed to EncryptFilesWithExtensionsNPE()!", err)
	}

	// Call the DecryptFilesWithExtensionsNPE function
	got, err := gotdf_python.DecryptFilesWithExtensionsNPE(tmpDir, []string{".tdf"}, gotdf_python.OpentdfConfig{
		ClientId:         config.npeClientId,
		ClientSecret:     config.npeClientSecret,
		PlatformEndpoint: config.platformEndpoint,
		TokenEndpoint:    config.tokenEndpoint,
		KasUrl:           config.kasEndpoint,
	}, defaultAuthScopes)
	if err != nil {
		t.Fatal("Failed to DecryptFilesWithExtensionsNPE()!", err)
	}

	if len(got) != numFiles {
		t.Fatal("DecryptFilesWithExtensionsNPE returned empty value, but didn't error!")
	}

	fmt.Println("Successfully decrypted files with extensions")
}

func createTestFiles(t *testing.T, tmpDir string) int {
	// A number that corresponds to the hour of the day (between 0 and 23)
	numFiles := time.Now().Hour()

	if numFiles > 12 {
		numFiles = numFiles - 12 // Limit the number of files to 12
	}

	for i := 0; i < numFiles; i++ {
		ext := ".txt"
		if i%2 == 0 {
			ext = ".csv"
		} else if i%3 == 0 {
			ext = ".pdf"
		}

		tmpFile, err := os.CreateTemp(tmpDir, fmt.Sprintf("input-file-%d-*%s", i, ext))
		if err != nil {
			t.Fatal("Could not create input file", err)
		}
		defer tmpFile.Close()

		// Write some data to the file
		if _, err = tmpFile.WriteString("test data"); err != nil {
			t.Fatal("Unable to write to temporary file", err)
		}
	}

	return numFiles
}
