package WeatherApp;
import io.appium.java_client.AppiumDriver;
import io.appium.java_client.MobileBy;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Parameters;
import org.testng.annotations.Test;
import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;

public class WeatherIos {
    AppiumDriver driver = null;
    //Xpath
    static String non_home_page = "//XCUIElementTypeButton[@name='Location List']";
    static String home_page = "//XCUIElementTypeStaticText[@name='Weather']";
    static String search_tab = "//XCUIElementTypeSearchField[@name='Search for a city or airport']";
    static String send_key_box = "//XCUIElementTypeSearchField[@name='Search for a city or airport']";
    static String list_item = "(//XCUIElementTypeButton[contains(@name,'%s')])[1]";
    static String Add = "//XCUIElementTypeButton[@name='Add']";
    static String setting_icon = "//XCUIElementTypeButton[@name='More']";
    static String edit_list = "//XCUIElementTypeButton[@name='Edit List']";
    static String delete_1 = "(//XCUIElementTypeButton[@name='Delete '])[1]";
    static String delete_2 = "//XCUIElementTypeButton[@name='Delete']";
    static String cancel = "//XCUIElementTypeButton[@name='Done']";
    static String get_temp = "(//XCUIElementTypeStaticText[contains(@name,\"°\")])[2]";
    static String[] names = {"Death Valley, California, USA","Kebili, Tunisia" , "Turbat, Pakistan",
            "Sudan,TX United States", "northern Mexico", "Bangkok, Thailand","Timbuktu, Mali", "Ghadames, Libya",
            "Phoenix, Arizona","Ethiopia Dubai"};

    @Parameters({"udid","url"})
    @BeforeTest
    public void BasicInitializer(String udid,String url) throws MalformedURLException {
        DesiredCapabilities desiredCapabilities = new DesiredCapabilities();
        desiredCapabilities.setCapability("automationName","xcuitest");
        desiredCapabilities.setCapability("udid",udid);
        desiredCapabilities.setCapability("bundleId","com.apple.weather");
        desiredCapabilities.setCapability("platformName","ios");
        desiredCapabilities.setCapability("deviceName","iPhone 8");
        desiredCapabilities.setCapability("headspin:capture.video",true);
        desiredCapabilities.setCapability("headspin:testName","WeatherIos");
        desiredCapabilities.setCapability("noReset", true);
        driver = new AppiumDriver(new URL(url),desiredCapabilities);
    }
    @Test
    public void method() throws InterruptedException {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(30));
        driver.manage();
        System.out.println("App Launch done");
        Thread.sleep(3000);

        // this is to verify the page is loaded
        try {
            WebElement PageElement = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(non_home_page)));
            PageElement.click();
            System.out.println("It's in home page");
        } catch (Exception e) {
            // Handle other types of exceptions
            System.out.println("It's in home page");
        }


        WebElement HomePageElement = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(home_page)));
        assert HomePageElement.isDisplayed() : "Element is not found.";
        for (String name : names) {
            //click on the search tab
            WebElement search_tab_c = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(search_tab)));
            search_tab_c.click();
            Thread.sleep(1500);

            // send the name for the search box
            WebElement search_filed = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(send_key_box)));
            search_filed.sendKeys(name);
            Thread.sleep(2300);

            //click the name for the actual element
            String name_new = name.substring(1, 4);
            String xpath_name = String.format(list_item,name_new);
            WebElement Pick_element = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(xpath_name)));
            Pick_element.click();
            Thread.sleep(3000);

            //add to the list
            WebElement add_location = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(Add)));
            add_location.click();
            Thread.sleep(2000);
            // 'name' takes on the value of each element in 'names'
            // Perform some action with 'name'
        }

        // select the setting icon
        Thread.sleep(2000);
        WebElement setting = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(setting_icon)));
        setting.click();
        Thread.sleep(1000);

        //select the edit list
        WebElement list = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(edit_list)));
        list.click();
        Thread.sleep(2000);
        int m = 0;

        while(true) {
            try {
                WebElement get_t = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(get_temp)));
                String t = get_t.getText();
                System.out.println(String.format("Temperature at %s is %s",names[m],t));
                m++;
                WebElement d1 = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(delete_1)));
                d1.click();
                Thread.sleep(2000);

                WebElement d2 = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(delete_2)));
                d2.click();
                Thread.sleep(2000);
            } catch (Exception e) {
                System.out.println("list is cleared");
                WebElement can = wait.until(ExpectedConditions.presenceOfElementLocated(MobileBy.xpath(cancel)));
                can.click();
                break;
            }
        }
    }
    @AfterClass
    public void tearDown() {
        driver.quit();
    }
}
