@REM Run tests & clean up
python src/automate.py
tasklist | find /i "chromedriver.exe" && taskkill /im chromedriver.exe /F || echo chromedriver is not running.
echo Finished running tests