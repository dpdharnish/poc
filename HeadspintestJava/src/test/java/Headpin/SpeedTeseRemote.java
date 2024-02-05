package Headpin;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;
public class SpeedTeseRemote {
    public static void main(String[] args) throws MalformedURLException {
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setBrowserName("firefox"); // Replace with the desired browser or device
        capabilities.setVersion("106.0.2"); // Specify the browser version// Specify the platform
        capabilities.setCapability("headspin:capture", true);
        WebDriver driver = new RemoteWebDriver(new URL("https://dev-us-pao-1.headspin.io:9095/v0/80baacf2d97e4bd29aa3a361775f0786/wd/hub"), capabilities);
        try {
            Duration timeout = Duration.ofSeconds(10);
            WebDriverWait wait = new WebDriverWait(driver, timeout);
            driver.get("https://www.speedtest.net");
            Thread.sleep(4000);
//            WebElement acceptCookiesButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[contains(text(),'Accept Cookies')]")));
//            acceptCookiesButton.click();
            // Find and click the second element with the specified XPath
            WebElement secondElement = driver.findElement(By.xpath("//span[@class='start-text']"));
            secondElement.click();
            String DOWNLOAD;
            while (true) {
                WebElement thirdElement = driver.findElement(By.xpath("(//span[contains(@class,'result-data-large')])[2]"));
                WebElement fourthElement = driver.findElement(By.xpath("(//span[contains(@class,'result-data-large')])[1]"));
                DOWNLOAD = thirdElement.getText();
                if (isNumeric(DOWNLOAD)) {
                    String num = fourthElement.getText();
                    System.out.println("UPLOAD speed in Mbps is " + num);
                    System.out.println("DOWNLOAD speed in Mbps is " + DOWNLOAD);
                    break;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // Close the browser
            driver.quit();
        }

    }
    public static boolean isNumeric(String str) {
        try {
            // Attempt to parse the string as a double
            Double.parseDouble(str);
            return true;
        } catch (NumberFormatException e) {
            // The string is not a number
            return false;
        }
    }
}


//https://ui.headspin.io/sessions/79eb639e-40ff-11ee-a8ae-06d8a473fcbf/waterfall