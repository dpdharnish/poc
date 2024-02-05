package Headpin;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.firefox.FirefoxDriver;
import java.time.Duration;
public class SpeedwebTest {
    public static void main(String[] args) {
        WebDriver driver = new FirefoxDriver();
        try {
            Duration timeout = Duration.ofSeconds(10);
            // Create an explicit wait with a timeout of 10 seconds
            WebDriverWait wait = new WebDriverWait(driver, timeout);
            driver.get("https://www.speedtest.net");
            // Wait for the "Accept Cookies" button to be clickable
            Thread.sleep(4000);
            WebElement acceptCookiesButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[contains(text(),'Accept Cookies')]")));
            acceptCookiesButton.click();
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
