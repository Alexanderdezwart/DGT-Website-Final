from flask import Flask, render_template, request
from config import Config
import sqlite3

app=Flask(__name__)

# Allows configuration like settings to be tucked away in a separate file.  See config.py
app.config.from_object(Config)

# Get the title of the website from Config and
# make it available to all templates. Used in
# header.html and layout.html in this case
@app.context_processor
def context_processor():
  return dict(title=app.config['TITLE'])


# The home page
@app.route('/')
def index():
  return render_template('index.html')


# Displays all weapons in the database
@app.route('/weapons')
def all_weapons():
  conn = sqlite3.connect(app.config['DATABASE'])
  cur = conn.cursor()
  cur.execute("SELECT * FROM CE")
  # fetchall returns a list of results
  weapons = cur.fetchall()
  conn.close()  # always close the db when you're done.
  return render_template("all_weapons.html", weapons=weapons)


# Individual teddy details page.
@app.route('/weapon/<int:GunID>')
def weapon_details(GunID):
  conn = sqlite3.connect(app.config['DATABASE'])
  cur = conn.cursor()
  cur.execute("SELECT CE.Name, Ammo.Gun, CE.WeaponFrame, DamageType.Damage, Ammo.AmmoType, CE.Impact, CE.Range, CE.Stability, CE.Handling, CE.ReloadSpeed, CE.AimAssistance, CE.Recoil, CE.RPM, CE.MagazineSize, CE.Rating, CE.Image FROM CE JOIN DamageType ON CE.DamageType=DamageType.DamageID JOIN Ammo ON CE.GunAmmo=Ammo.GunAmmoID WHERE CE.GunID =?;",(GunID,))
   # fetchone returns a tuple containing the data for one entry
  weapon = cur.fetchall() 
  if len(weapon)<=0:
    # determines if the GUNID being inputted actually exists
    message = "Sorry this weapon could not be found."
    conn.close()
    return render_template('error.html', message=message)
  conn.close()
  return render_template("weapon.html", weapon=weapon)


  

@app.route('/about_feedback', methods=['POST'])
def submit_feedback():
  conn = sqlite3.connect(app.config["DATABASE"])
  cur = conn.cursor()
  cur.execute("INSERT INTO Feedback (Feedback) VALUES (?)", [request.form["Feedback"]])
  conn.commit()
  conn.close()
  return render_template('about.html')


@app.route("/about")
def about():
  return render_template('about.html')

@app.errorhandler(404)
def invalidroute(e):
  message = "Sorry this page could not be found."
  return render_template('error.html', message=message)


if __name__ == '__main__':
  app.run(debug=app.config['DEBUG'], port=8880, host='0.0.0.0') 