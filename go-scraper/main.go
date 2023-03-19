package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

func fetch(url string) ([]byte, error) {
	response, err := http.Get(url)
	if err != nil {
		return []byte{}, err
	}

	if response.StatusCode != 200 {
		return []byte{}, errors.New(fmt.Sprintf("Status code expected 200, received: %d", response.StatusCode))
	}

	raw, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return []byte{}, err
	}

	return raw, nil
}

func createFolderIfNotExists(folderPath string) error {
	if _, err := os.Stat(folderPath); errors.Is(err, os.ErrNotExist) {
		fmt.Printf("Cache file does not exist, creating %s\n", folderPath)
		if err := os.Mkdir(folderPath, os.ModePerm); err != nil {
			return err
		}
	}

	return nil
}

func saveToCache(filePath string, body []byte) error {
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}

	defer file.Close()

	_, err = file.Write(body)
	if err != nil {
		return err
	}

	return nil
}

func getCachePath() string {
	if val, exists := os.LookupEnv("CACHE_PATH"); exists {
		if val[len(val)-1:] == "/" {
			return val[:len(val)-1]
		}

		return val
	}

	return "./cache"
}

func scrape(symbol string) error {

	cacheFilePath := fmt.Sprintf("%s/ticker_%s.json", getCachePath(), strings.ToUpper(symbol))

	if valid, err := isCacheValid(cacheFilePath); err == nil && valid {
		fmt.Println(fmt.Sprintf("Cache has not expired for %s", symbol))
		return nil
	}

	fmt.Println(fmt.Sprintf("Fetching data from API for symbol %s", symbol))

	raw, err := fetch(fmt.Sprintf("https://query2.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=assetProfile,balanceSheetHistory,balanceSheetHistoryQuarterly,calendarEvents,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,earnings,earningsHistory,earningsTrend,financialData,fundOwnership,incomeStatementHistory,incomeStatementHistoryQuarterly,indexTrend,industryTrend,insiderHolders,insiderTransactions,institutionOwnership,majorDirectHolders,majorHoldersBreakdown,netSharePurchaseActivity,price,quoteType,recommendationTrend,secFilings,sectorTrend,summaryDetail,summaryProfile,symbol,upgradeDowngradeHistory,fundProfile,topHoldings,fundPerformance", symbol))
	if err != nil {
		return err
	}

	if err := saveToCache(cacheFilePath, raw); err != nil {
		return err
	}

	return nil
}

func isCacheValid(filePath string) (bool, error) {
	file, err := os.Stat(filePath)

	if err != nil {
		return false, err
	}

	modifiedTime := file.ModTime()

	today := time.Now()
	expireTime := modifiedTime.Add(24 * time.Hour)

	return today.Before(expireTime), nil
}

func main() {
	start := time.Now()

	symbols := os.Args[1:]

	absPath, err := filepath.Abs(getCachePath())
	if err != nil {
		log.Fatal(err)
	}

	if err := createFolderIfNotExists(absPath); err != nil {
		log.Fatal(err)
	}

	wg := sync.WaitGroup{}

	for _, symbol := range symbols {
		wg.Add(1)
		go func(symbol string) {
			if err := scrape(symbol); err != nil {
				fmt.Println(fmt.Sprintf("Error while fetchin %s: %v", symbol, err))
			}
			wg.Done()
		}(symbol)
	}

	wg.Wait()

	elapsed := time.Since(start)
	log.Printf("Execution took %s", elapsed)
}
