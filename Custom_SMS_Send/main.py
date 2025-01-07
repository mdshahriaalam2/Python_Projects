from flask import Flask, request
import requests
import json

app = Flask(__name__)

class SMSClient:
    def __init__(self, phn, sms):
        self.phn = phn
        self.sms = sms
        self.url = "http://202.51.182.198:8181/nbp/sms/code"
        self.headers = {
            "Authorization": "Bearer",
            "Language": "en",
            "Timezone": "Asia/Dhaka",
            "Content-Type": "application/json; charset=utf-8",
            "Content-Length": "137",
            "Host": "202.51.182.198:8181",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"
        }

    def send_sms(self):
        data = {
            "receiver": self.phn,
            "text": self.sms,
            "title": "Register Account"
        }

        response = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phn = request.form['phn']
        sms = request.form['sms']
        client = SMSClient(phn, sms)
        response = client.send_sms()
        # Removed the line to hide the form section
        return '''
        <!DOCTYPE html>
        <html lang="en">
        
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SMS Sender</title>
            <style>
                form {
                    margin: 20px auto;
                    padding: 20px;
                    border: 1px solid #ccc;
                    max-width: 400px;
                    border-radius: 5px;
                }
        
                input[type="text"],
                textarea {
                    width: 100%;
                    padding: 12px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    box-sizing: border-box;
                    font-size: 18px;
                    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
                }
        
                label {
                    font-size: 18px;
                    font-weight: bold;
                }
        
                input[type="submit"],
                input[type="button"] {
                    background-image: linear-gradient(white, red, green);
                    color: white;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    opacity: 0.8;
                    transition: opacity 0.3s;
                }
        
                input[type="submit"]:hover,
                input[type="button"]:hover {
                    opacity: 1;
                }
            </style>
            <script>
                function clearForm() {
                    document.getElementById("phn").value = "01";
                    document.getElementById("sms").value = "";
                }
        
                function validatePhoneNumber() {
                    var phn = document.getElementById("phn").value;
                    if (phn.length !== 11) {
                        alert("Phone number must be 11 digits long.");
                        return false;
                    }
                    return true;
                }
            </script>
        </head>
        
        <body>
            <form method="post">
                <label for="phn">Phone Number:</label><br>
                <input type="text" id="phn" name="phn" placeholder="01XXXXXXXXX" required><br>
                <label for="sms">SMS Text:</label><br>
                <textarea id="sms" name="sms" rows="4" required></textarea><br><br>
                <input type="submit" value="Send Message">
                <input type="button" value="Clear Form" onclick="clearForm()">
                <br><br>
                <p>Message sent successfully</p> <!-- Success message -->
            </form>
        </body>
        
        </html>
        '''  # Injecting the response into the HTML
    return '''
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SMS Sender</title>
        <style>
            form {
                margin: 20px auto;
                padding: 20px;
                border: 1px solid #ccc;
                max-width: 400px;
                border-radius: 5px;
            }
    
            input[type="text"],
            textarea {
                width: 100%;
                padding: 12px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
                font-size: 18px;
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }
    
            label {
                font-size: 18px;
                font-weight: bold;
            }
    
            input[type="submit"],
            input[type="button"] {
                background-image: linear-gradient(white, red, green);
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                opacity: 0.8;
                transition: opacity 0.3s;
            }
    
            input[type="submit"]:hover,
            input[type="button"]:hover {
                opacity: 1;
            }
        </style>
        <script>
            function clearForm() {
                document.getElementById("phn").value = "01";
                document.getElementById("sms").value = "";
            }
    
            function validatePhoneNumber() {
                var phn = document.getElementById("phn").value;
                if (phn.length !== 11) {
                    alert("Phone number must be 11 digits long.");
                    return false;
                }
                return true;
            }
        </script>
    </head>
    
    <body>
        <form method="post">
            <label for="phn">Phone Number:</label><br>
            <input type="text" id="phn" name="phn" placeholder="01XXXXXXXXX" required><br>
            <label for="sms">SMS Text:</label><br>
            <textarea id="sms" name="sms" rows="4" required></textarea><br><br>
            <input type="submit" value="Send Message">
            <input type="button" value="Clear Form" onclick="clearForm()">
        </form>
    </body>
    
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
