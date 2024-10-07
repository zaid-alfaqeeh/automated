from flask import Flask, render_template
from flask_cors import CORS
from splinter import Browser
import time
import os 

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')  # This will render the HTML page

@app.route('/start-script')
def start_script():
    with Browser('chrome') as browser:
        browser.visit('https://services.just.edu.jo/sturegistration/Reg/Default.aspx')
        time.sleep(5)
        browser.fill("txtStuNo", "1")
        browser.fill("txtPassword", "")
        try:
            browser.find_by_id("recaptcha-anchor").click()
        except:
            time.sleep(0)
        browser.find_by_name("btnLogin").click()

        stop = False
        while True:
            browser.find_by_name('ctl00$cphBody$gvCourses$ctl06$btnViewAvailableSection').click()
            time.sleep(2)
            rows = browser.find_by_css('tr.GridRowClass, tr.GridAlternatingRowClass')
            for row in rows:
                class_number = row.find_by_tag('td')[0].text
                if class_number == "33":
                    print(class_number)
                    browser.find_by_css('.ui-button').click()
                    browser.fill("ctl00$cphBody$gvCourses$ctl06$txtNewSectionNo", class_number)
                    browser.find_by_name("ctl00$cphBody$gvCourses$ctl06$btnChangeSection").click()
                    stop = True
                    break
            if stop:
                break
            browser.find_by_css('.ui-button').click()
            time.sleep(5)

    return "Script completed."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
