const puppeteer = require('puppeteer-core');

async function launchBrowser() {
  return puppeteer.launch({
    executablePath: '/usr/bin/chromium',
    args: [
      '--user-data-dir=/home/so1omon/autonomous-ai/.chromium',
      '--no-sandbox',
      '--disable-gpu',
      '--headless',
    ],
  });
}

module.exports = { launchBrowser };
