import { defineConfig, devices } from "@appwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  
  use: {
    baseURL: "https://app-automate.browserstack.com",
    trace: "on-first-retry",
  },

  projects: [
    {
      name: "browserstack-android",
      use: {
        ...devices["Pixel 7"],
        // BrowserStack specific configuration
        browserName: "chrome",
        browserVersion: "latest",
        os: "android",
        osVersion: "13.0",
        deviceName: "Samsung Galaxy S23",
        realMobile: true,
        browserstackLocal: false,
        browserstackDebug: true,
        browserstackNetworkLogs: true,
        browserstackConsoleLogs: true,
        browserstackAppiumLogs: true,
        browserstackDeviceLogs: true,
        browserstackVideo: true,
        browserstackBuildName: "QualGent Test Build",
        browserstackProjectName: "QualGent Coding Challenge",
        browserstackSessionName: "Appwright Test Session",
        browserstackUserName: process.env.BROWSERSTACK_USERNAME,
        browserstackAccessKey: process.env.BROWSERSTACK_ACCESS_KEY,
      },
    },
    {
      name: "browserstack-ios",
      use: {
        ...devices["iPhone 14"],
        // BrowserStack specific configuration
        browserName: "safari",
        browserVersion: "latest",
        os: "ios",
        osVersion: "16",
        deviceName: "iPhone 14",
        realMobile: true,
        browserstackLocal: false,
        browserstackDebug: true,
        browserstackNetworkLogs: true,
        browserstackConsoleLogs: true,
        browserstackAppiumLogs: true,
        browserstackDeviceLogs: true,
        browserstackVideo: true,
        browserstackBuildName: "QualGent Test Build",
        browserstackProjectName: "QualGent Coding Challenge",
        browserstackSessionName: "Appwright Test Session",
        browserstackUserName: process.env.BROWSERSTACK_USERNAME,
        browserstackAccessKey: process.env.BROWSERSTACK_ACCESS_KEY,
      },
    },
  ],

  webServer: {
    command: "python -c \"import uvicorn; uvicorn.run('job_server.main:app', host='0.0.0.0', port=8000, reload=True)\"",
    url: "http://localhost:8000",
    reuseExistingServer: !process.env.CI,
  },
});