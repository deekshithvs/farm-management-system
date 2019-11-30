from flask import Flask ,redirect,url_for,request,render_template,session,flash
import datetime
import mysql.connector
import Analysis as an
import os
import smtplib
from pymongo import MongoClient
#import imgdetect as id
# import imgdetect as imgrec
import re 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

app=Flask(__name__)
@app.route('/')
def index():
        if not session.get('logged in'):
                return render_template('index.html',title='index',error = "") 
        else:
                return render_template('index.html',title='index',error = "")     
        return render_template('index.html',title='index',error = "")     
@app.route('/home/<string:type>/<string:id>')
def home(type,id):
        if(type=="Farmer"):
                return render_template('farmer.html',type =type,id = id)
        elif(type=="Consumer"):
                return render_template('consumer.html',type = type,id = id)
        else:
                return render_template('company.html',type = type,id = id)

@app.route('/login',methods = ['GET','POST'])
def login():
	if request.method == 'POST':
                email = request.form['email']
                if(  re.search(regex,email)):
                        print("valid email")
                else:
                        flash("invalid email...")
                        return render_template('login.html')

                passw = request.form['pas']
                print(passw)
                cur = db.cursor()
                cur.execute('SELECT usertype FROM loginAuth WHERE email = %s AND password = %s', (email, passw))
                acc = cur.fetchone()
                cur.execute('SELECT loginId FROM loginAuth WHERE email = %s AND password = %s', (email, passw))
                conid = cur.fetchone()
                if(acc): 
                        if(acc[0] == 'Farmer'):
                                session['logged_in']=True
                                flash('You were successfully logged in')
                                return render_template('farmer.html',type = 'Farmer',id = email)
                        elif acc[0] == 'Consumer':
                                flash('You were successfully logged in')
                                return render_template('consumer.html',type = 'Consumer', id = email)
                        else:
                                flash('You were successfully logged in')
                                return render_template('company.html',type = 'Company', id = email)
                else:
                        flash("Invalid Credentials",category='alert')
                        return redirect(url_for('login'))
	else:
                return render_template('login.html')
         

@app.route('/logout',methods = ['GET','POST'])
def logout():
        session['logged_in']=False
        return redirect(url_for('login'))

@app.route('/Register',methods=['GET','POST'])
def Register():
        if (request.method=='POST'):
                user=request.form["username"]
                email=request.form["email"]
                password=request.form["password"]
                userType=request.form["userType"]
                if( re.search(regex,email)):
                        print("valid email..")
                else:
                        flash("invalid email...")
                        return render_template('Register.html')

                query ="""insert into loginauth values(%s,%s,%s,%s)"""
                values=(email,password,userType,email)
                try:
                        cur=db.cursor()
                        cur.execute(query,values)
                        db.commit()
                        cur.close()
                        message = "Your Registration is completed"
                        try:
                                s.sendmail("farmcirclesupporoficial@gmail.com", email, message) 
                        except:
                                print("unable to send email")
                        finally:
                                flash('You Registered Succesfully and confirmation mail is sent')
                                return render_template('CreateProfile.html',title='Register',data=[],userType=userType,userEmail=email,firstName=user)
                except Exception as e:
                        print(e)
                        flash('Email is Already Registered..')
                        return redirect(url_for('Register'))

        else:
                return render_template('register.html')
                
       
       # return render_template('login.html',title='Register')

# # craeting profile details
@app.route('/CreateProfile/<string:type>/<string:email>/<string:firstName>/<int:flag>',methods=['POST'])
def CreateProfile(type,email,firstName,flag):
        print("creating profile")
        print(firstName)
        if(request.method=='POST'):
                last_Name=request.form["lastName"]
                state=request.form["state"]
                district=request.form["district"]
                city=request.form["city"]
                villageName=request.form["villageName"]
                pin=request.form["pin"]
                phoneNumber=request.form["phoneNumber"]
                profilePhoto=request.form["photo"]
                print(profilePhoto)
                cur=db.cursor()
                if(flag==0):
                        query='INSERT INTO UserProfile(email,usertype,firstname,lastName,state,district,city,villageName,pin,phoneNumber,profilePhoto) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
                        values=(email,type,firstName,last_Name,state,district,city,villageName,pin,phoneNumber,profilePhoto)
                        cur.execute(query,values)
                        db.commit()
                        print("adding data...")
                        if(type=="Farmer"):
                                print("farmer")
                                query='INSERT INTO farmerInfo(email,firstname,lastName,state,district,city,pin,phoneNumber) values(%s,%s,%s,%s,%s,%s,%s,%s)' 
                                values=(email,firstName,last_Name,state,district,city,pin,phoneNumber)
                                cur.execute(query,values)
                                db.commit()
                        elif(type=="Company"):
                                print("comapny")
                                query='INSERT INTO companyInfo(email,firstname,lastName,state,district,city,pin,phoneNumber) values(%s,%s,%s,%s,%s,%s,%s,%s)' 
                                values=(email,firstName,last_Name,state,district,city,pin,phoneNumber)
                                cur.execute(query,values)
                        else:
                                print("consumer")
                                query='INSERT INTO consumerInfo(email,firstname,lastName,state,district,city,pin,phoneNumber) values(%s,%s,%s,%s,%s,%s,%s,%s)' 
                                values=(email,firstName,last_Name,state,district,city,pin,phoneNumber)
                                cur.execute(query,values)
                        print("end...")


                elif(flag==1):
                        print("inside update....")
                        query="""update  UserProfile set firstname=%s,lastName=%s,state=%s,district=%s,city=%s,villageName=%s,pin=%s,phoneNumber=%s,profilePhoto=%s where email=%s"""
                        values=(firstName,last_Name,state,district,city,villageName,pin,phoneNumber,profilePhoto,email)
                        cur.execute(query,values)
                        db.commit()
                        flash("profile updated sucessfully...")
                try:
                        print(query)
                        print(values)
                        #cur.execute(query,values)
                        if(type=="Farmer"):
                                return render_template('farmer.html',type = "Farmer",id = email)
                        elif(type=="Company"):
                                return render_template('company.html',type = "Company",id = email)
                        else:
                                return render_template('Consumer.html',type = "Consumer",id = email)
                except:
                        flash('Email is Already Registered..')
                        return render_template('CreateProfile.html',type=type,email=email)
                finally:
                        cur.close()
        else:
                return render_template('CreateProfile.html',type=type,email=email)

@app.route('/plantDiseaseRecognition/<string:type>/<string:email>',methods=['POST','GET'])
def plantDiseaseRecognition(type,email):
        if(request.method=='POST'):
                cropImageURL=request.form["imageURL"]
                ImageURL=request.form["imageURL"]
                print(cropImageURL)
                #cur=db.cursor()
                # cropImageURL="C:\\Users\deekshith\Desktop\\"+cropImageURL
                # query='INSERT INTO  DiseaseRecognition(email,usertype,imageURL,time)  values(%s,%s,%s,%s)'
                # values=(email,type,cropImageURL,datetime.datetime.now())
                # cur.execute(query,values)
                # db.commit()
                print(type)
                print(email)
                #img=imgrec.image()
                import imgdetect as id
                img=id.image()
                #print(imageURL)
                cropImageURL="C:\\Users\deekshith\Desktop\project-5th sem\\farmcircle\static\img\\"+cropImageURL
                res=img.predict(cropImageURL)
                #print(cropImageURL)
                #res=id.convert_image_to_array(cropImageURL)
                print(res)
                res=str(res)
                diseasedb= db1["diseaseDetails"]
                #res=img.predict(cropImageURL)
                data=diseasedb.find_one({"name":res})
                print(data)
                return render_template('displaydiseaseDetails.html',data=data,image=ImageURL,name=res)
                
        return render_template('login.html')


@app.route('/AddCrops/<string:type>/<string:email>',methods=['GET','POST'])
def AddCrops(type,email):
        if(request.method=='POST'):
                cropType=request.form["cropType"]
                cropName=request.form["cropName"]
                quantity=request.form["quantity"]
                rates=request.form["rates"]
                print(cropName)
                cropImageURL=request.form["imageURL"]
                cur=db.cursor(cropImageURL)
                print(cropImageURL)
                query='INSERT INTO productDetails(Email,CropType,Cropname,Rate,Quantity,imageUrl,usertype,time) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                values=(email,cropType,cropName,quantity,rates,cropImageURL,type,datetime.datetime.now())
                try:
                        cur.execute(query,values)
                        db.commit()
                        flash('Crop added successfully')
                except Exception as e:
                        flash("something went wrong ....Product is not added")
                        print(e)
                        return render_template('farmer.html',type=type,id=email)
                finally:
                        cur.close()
                if(cur!=None):
                        print("!product added")
                        return render_template('farmer.html',type=type,id=email)
                else:
                        print("not added")
                        return render_template('addCrops.html',title='Addccrops',userType=type,userEmail=email)
        else:
                return render_template('addCrops.html',title='Addccrops',type=type,id=email)

@app.route('/profile/<string:type>/<string:id>',methods=['GET','POST'])
def profile(type,id):
        cur=db.cursor()
        print(id)
        query="""select * from UserProfile where email=%s"""
        cur.execute(query,(id,))
        if(cur!=None):
                print("sucess")
                datas=cur.fetchone()
                print(datas)
                #cur.close()
                return render_template('profile.html',userType=type,userEmail=id,data=datas,firstName=datas[2])
        else:
                print("No Items to display")
                cur.close()
                return render_template('index.html',userType=type,userEmail=id)

@app.route('/displayCrops/<string:type>/<string:id>',methods = ['GET','POST'])
def display(type,id):
        cur = db.cursor()
        # query = 'SELECT * FROM productdetails'
        # query="SELECT * FROM productdetails"
        # query='SELECT * FROM productdetails where email= \'farmer\' '
        cur.execute('SELECT a.Email,a.CropType,a.CropName,a.Rate,a.Quantity,a.CropID,a.imageUrl,a.usertype,a.time,b.phonenumber FROM productdetails as a inner join userprofile as b on a.Email=b.email and a.quantity>0')
        data = cur.fetchall()
        # cur.execute('select phonenumber from userprofile where email=%s',(data[0],))
        # phonenumber=cur.fetchone()
        # print(phoneNumber)
        if(len(data)>0):
                cur.close()
                return render_template('product.html', data = data,fid = id,type=type)
        else:
                flash("there is no product to display")
                cur.close()
                return render_template('consumer.html',id=id,type=id)

# my crops for farmer
@app.route('/myproduct/<string:type>/<string:id>',methods = ['GET','POST'])
def myproduct(type,id):
        print(type)
        cur = db.cursor()
        if(str(type)):
                print(id)
                query="""SELECT * FROM productdetails where Email=%s and quantity>0"""
                value=(id,)
                cur.execute(query,value)
                data = cur.fetchall()
                cur.close()
                print("modifycrops.html")
                if(len(data)>0):
                        return render_template('modifycrops.html',type=type, data = data,id = id)
                else:
                        flash("no Crops to dispaly")
                        return render_template('farmer.html',id=id,type=type)
        else:
                return render_template('farmer.html',type=type,id = id)

@app.route('/requestsDisplay/<string:type>/<string:id>',methods = ['GET','POST'])
def requestsDisplay(type,id):
        print(id)
        if(str(type)=="consumer" or str(type)=="Consumer"):
                print("cosumer")
                cur = db.cursor()
                query="""SELECT * FROM productdetails where Email=%s"""
                value=(id,)
                cur.execute('SELECT farmerID,quantity,cropName,rate,cropID,date,status,id FROM requests where consumerID =%s',(id,))
                data = cur.fetchall()
                cur.close()
                #cur.close()
                print(data)
                print("fetching details of consumer requests")
                if(len(data)>0):
                        return render_template('displaycropRequest.html',type=type, data = data,id = id)
                else:
                        flash("there is no product to display")
                        return render_template('consumer.html',id=id,type=id)
        elif(str(type)=="Farmer"):
                cur = db.cursor()
                cur.execute('SELECT a.companyID,a.quantity,a.rate,b.fertilizerName,a.date,a.status ,a.id ,b.imageUrl FROM requestfert as a inner join fertilizerdetails as b on b.fertilizer_ID=a.fertID and  farmerID =%s',(id,))
                data = cur.fetchall()
                #cur.close()
                print(data)
                cur.close()
                if(len(data)>0):
                        print("fetching details of consumer requests")     
                        return render_template('displayFertiRequests.html',type=type, data = data,id = id)
                else:
                        flash("no Product to display..")
                        return render_template('farmer.html',type=type,id=id)
        else:
                return render_template('consumer.html',id=id,type=id)

@app.route('/requestsfeedback/<string:type>/<string:id>',methods = ['GET','POST'])
def myfeedbackfert(type,id):
        if(type=="Farmer"):
                cur = db.cursor()
                cur.execute('SELECT a.companyID,a.quantity,a.rate,b.fertilizerName,a.date,a.status ,a.id FROM requestfert as a inner join fertilizerdetails as b on b.fertilizer_ID=a.fertID and  farmerID =%s and a.status=true',(id,))
                data = cur.fetchall()
                #cur.close()
                print(data)
                cur.close()
                if(len(data)>0):
                        print("fetching details of consumer requests")
                        return render_template('displayFertiFeedback.html',type=type, data = data,id = id)
                else:
                        flash("no Product to give feedback..")
                        return render_template('Farmer.html',type=type,id=id)
        else:
                print("consumer")
                cur = db.cursor()
                # query="""SELECT * FROM productdetails where Email='abcd'"""
                # value=(id,)
                cur.execute('SELECT farmerID,quantity,cropName,rate,cropID,date,status,id FROM requests where consumerID =%s and status =true',(id,))
                data = cur.fetchall()
                cur.close()
                #cur.close()
                print(data)
                print("fetching details of consumer requests")
                if(len(data)>0):
                        return render_template('displayCropFeedback.html',type=type, data = data,id = id,)
                else:
                        flash("there are no products  for feedback...")
                        return render_template('consumer.html',id=id,type=id)
#my feriizer
@app.route('/myfert/<string:type>/<string:email>',methods = ['GET','POST'])
def myfeedbackcrop(type,email):
        try:    
                print("myfert")
                cur = db.cursor()
                print(id)
                cur.execute('SELECT * FROM fertilizerdetails where Email =%s',(email,))
                data = cur.fetchall()
                print(data)
                cur.close()
                if(len(data)>0):
                        return render_template('modifyfert.html', data = data,fid = email,type=type)
                else:
                        flash("No product to display")
                        return render_template('company.html',id = email,type=type)
        except Exception as e:
                flash("something went wrong ..")
                return render_template('company.html',id = email,type=type)     

@app.route('/feedbacks/<string:id>/<string:consumer>/<int:itemid>',methods=['POST','GET'])
def myfeedbacdisplay(id,consumer,itemid):
        return render_template('feed.html',id = id, type = consumer,item = itemid)

@app.route('/feedback/<string:id>/<string:consumer>/<string:itemid>',methods = ['GET','POST'])
def myfeedback(id,consumer,itemid):
        if (request.method =='POST'):
                experience = request.form['experience']
                name = request.form['name']
                email = request.form['email']
                comments = request.form['comments']
                query="""select farmerID from requests where id=%s"""
                cur=db.cursor()
                values=(id,)
                cur.execute(query,values)
                data=cur.fetchone()
                #farmerID=data[0]
                print(itemid)
                dict={"experience":experience,"Name":name,"email":email,"comments":comments,"item":itemid,"about_email":itemid}
                feed.insert_one(dict)
                flash("Feed back is added sucessfully......")
                return render_template("consumer.html",type = consumer,id = id)
                return render_template("feed.html",id = id, type = consumer,item = itemid)
        else:
                return render_template("feed.html",id = id, type = consumer,item = itemid)


@app.route('/plantrec')
def plantrec():
        return render_template('plant image_recogn.html')

@app.route('/checkreview/<string:id>/<string:itemid>',methods = ['GET','POST'])
def checkreview(id,itemid):
        # query="""select farmerID from requests where id=%s"""
        # cur=db.cursor()
        # values=(itemid,)
        # cur.execute(query,values)
        # data=cur.fetchone()
        # farmerID=data[0]
        #print(farmerID)
        x = feed.find({"about_email":itemid})
        print(x)
        return render_template('dash.html', data = x)
        # e
        #lse:
        #         flash("No reviews yet")
        #         return render_template("consumer.html",type = "Consumer",id  = id)



@app.route('/cropOrder/<string:id>/<string:cropid>',methods=['POST'])
def croporder(id,cropid):
        quantity=request.form['req_quantity']
        try:
                cur = db.cursor()
                print(cur)
                query='SELECT Email,Cropname,Rate,Quantity FROM productdetails where cropID =%s'
                values=(cropid,)
                cur.execute(query,values)
                data = cur.fetchone()
                query="""insert into requests(farmerID,quantity,date,cropName,status,rate,cropID,consumerID) values(%s,%s,%s,%s,false,%s,%s,%s)"""
                values=(data[0],quantity,datetime.datetime.now(),data[1],data[2],cropid,id)
                cur.execute(query,values)
                db.commit()
                query="""update productdetails set quantity=%s where cropid=%s"""
                quantity=int(data[3])-int(quantity)
                values=(quantity,cropid)
                flash("product is placed successfully..")
                flash("Further information will be provide through the email..")
                cur.execute(query,values)
                print(data)
                cur.execute('SELECT a.Email,a.CropType,a.CropName,a.Rate,a.Quantity,a.CropID,a.imageUrl,a.usertype,a.time,b.phonenumber FROM productdetails as a inner join userprofile as b on a.Email=b.email and a.quantity>0')
                data = cur.fetchall()
                cur.close()
                return render_template('product.html',data = data,fid =id)
        except Exception as e:
                return str(e)
        finally:
                cur.close()
        return "failed"

@app.route('/fertOrder/<string:id>/<string:fertid>',methods=['POST'])
def fertorder(id,fertid):
        quantity=request.form['req_quantity']
        try:
                cur = db.cursor()
                print(fertid)
                query='SELECT * FROM fertilizerdetails where fertilizer_ID =%s'
                values=(fertid,)
                cur.execute(query,values)
                data = cur.fetchone()
                query="""insert into  requestfert(companyID,quantity,date,status,rate,fertID,farmerID) values(%s,%s,%s,false,%s,%s,%s)"""
                values=(data[0],quantity,datetime.datetime.now(),data[4],fertid,id)
                cur.execute(query,values)
                db.commit()
                quantity=int(data[3])-int(quantity)
                query="""update fertilizerdetails set quantity=%s where fertilizer_ID=%s"""
                values=(quantity,fertid)
                cur.execute(query,values)
                db.commit()
                cur.execute('SELECT a.email,a.fertilizerName,a.Rate,a.Quantity,a.fertilizer_ID,a.imageUrl,a.time,b.phonenumber FROM fertilizerdetails as a inner join userprofile as b on a.email=b.email and a.quantity>0')
                data = cur.fetchall()
                print(data)
                print("redirecting to dispalyFert.html ")
                cur.close()
                flash('Order placed successfully')
                flash("further information is send through email...")
                return render_template('dispalyFert.html', data = data,fid = id)
        except Exception as e:
                return str(e)
        return "failed"

@app.route('/deletecrop/<string:fid>/<string:cropid>')
def deletecrop(fid,cropid):
        print(fid)
        try:
                cur = db.cursor()
                print(cropid)
                query='delete from productdetails where CropID=%s'
                values=(cropid,)
                flash("Crop deleted succesfully")
                cur.execute(query,values)
                data = cur.fetchone()
                query="""SELECT * FROM productdetails where Email=%s and Quantity>0"""
                value=(fid,)
                cur.execute(query,value)
                data = cur.fetchall()
                cur.close()
                print("modifycrops.html")
                if(len(data)>0):
                        return render_template('modifycrops.html',type=type, data = data,id = fid)
                else:
                        flash("no Crops to dispaly")
                        return render_template('farmer.html',id=id,type=type)
        except Exception as e:
                print(e)
                cur = db.cursor()
                query="""SELECT * FROM productdetails where Email=%s"""
                value=(fid,)
                cur.execute(query,value)
                data = cur.fetchall()
                cur.close()
                flash("crop deleted was unsuccesful...")
                print("redicting to modifycrop.html")
                return render_template('modifycrops.html',type=type, data = data,id = fid)
        finally:
                cur.close()

@app.route('/cancel/<string:id>/<string:type>/<string:reqid>',methods=["POST","GET"])
def cancelRequest(id,type,reqid):
        print(id)
        try:
                cur = db.cursor()
                print(reqid)
                if(type=="Farmer"):
                        print("Farmer")
                        query="""delete from requestfert where id=%s"""
                        values=(reqid,)
                        cur.execute(query,values)
                else:
                        print("Consumer")
                        query='delete from requests where id=%s'
                        values=(reqid,)
                        cur.execute(query,values)
                flash('Product Cancelled successfully')
                db.commit()
                print("deleted")
                if(type=="Consumer"):
                        print("cosnumer")
                        cur.execute('SELECT farmerID,quantity,cropName,rate,cropID,date,status,id FROM requests where consumerID =%s',(id,))
                        data = cur.fetchall()
                        #cur.close()
                        print(data)
                        print("fetching details of consumer requests")
                        return render_template('displayCropRequest.html',type=type, data = data,id = id)
                else:
                        print("farmer")
                        cur.execute('SELECT a.companyID,a.quantity,a.rate,b.fertilizerName,a.date,a.status ,a.id ,b.imageUrl FROM requestfert as a inner join fertilizerdetails as b on b.fertilizer_ID=a.fertID and  farmerID =%s',(id,))
                        data = cur.fetchall()
                        #cur.close()
                        print(data)
                        print("fetching details of consumer requests")
                        return render_template('displayFertiRequests.html',type=type, data = data,id = id)
                        return render_template('modifycrops.html',type=type, data = data,id = id)
        except Exception as e:
                return str(e)
        finally:
                cur.close()


@app.route('/deletefert/<string:email>/<string:fertid>')
def deletefert(email,fertid):
        print(id)
        try:
                cur = db.cursor()
                print(fertid)
                query="""delete from fertilizerdetails where fertilizer_ID=%s"""
                values=(fertid,)
                cur.execute(query,values)
                db.commit()
                cur.execute('SELECT * FROM fertilizerdetails where Email =%s',(email,))
                data = cur.fetchall()
                print(data)
                cur.close()
                flash('Product deleted  successfully')
                return render_template('modifyfert.html', data = data,fid = email)
        except:
                return render_template('company.html', id=email,type= "Company")
                

@app.route('/update_a_crops/<string:email>/<string:cropid>',methods=["POST"])
def update_A_crop(email,cropid):
        print("hello")
        if(request.method=='POST'):
                try:
                        # cropType=request.form["cropType"]
                        # print("crops")
                        # cropName=request.form["cropName"]
                        quantity=request.form["quantity"]
                        rates=request.form["rates"]
                        print(rates)
                        cropImageURL=request.form["imageURL"]
                        cur=db.cursor()
                        query="""update  productDetails set Quantity=%s,Rate=%s,imageUrl=%s, time=%s where CropID=%s"""
                        values=(quantity,rates,cropImageURL,datetime.datetime.now(),cropid)
                        cur.execute(query,values)
                        db.commit()
                        print(cropid)
                        query="""SELECT * FROM productdetails where Email='abcd'"""
                        value=(id,)
                        cur.execute('SELECT * FROM productdetails where email =%s',(email,))
                        data = cur.fetchall()
                        print("modify.html")
                        cur.close()
                        flash('Product updated  successfully')
                        return render_template('modifycrops.html',type=type, data = data,id = email)
                except Exception as e:
                        cur=db.cursor()
                        query="""SELECT * FROM productdetails where Email='abcd'"""
                        value=(id,)
                        cur.execute('SELECT * FROM productdetails where email =%s',(email,))
                        data = cur.fetchall()
                        print("modify.html")
                        cur.close()
                        flash('Product updated  was unsuccessful..please try it again')
                        return render_template('modifycrops.html',type=type, data = data,id = email)
                        return str(e)
                finally:
                        cur.close()


@app.route('/update_a_fert/<string:email>/<string:fertid>',methods=["POST"])
def update_A_fert(email,fertid):
        print("hello")
        if(request.method=='POST'):
                try:
                        # cropType=request.form["cropType"]
                        # print("crops")
                        # cropName=request.form["cropName"]
                        quantity=request.form["quantity"]
                        rates=request.form["rates"]
                        print(rates)
                        fertImageURL=request.form["imageURL"]
                        fertImageURL="C:\\Users\deekshith\Documents\\"+fertImageURL
                        cur=db.cursor()
                        query="""update  fertilizerdetails set Quantity=%s,Rate=%s,imageUrl=%s, time=%s where fertilizer_ID=%s"""
                        values=(quantity,rates,fertImageURL,datetime.datetime.now(),fertid)
                        cur.execute(query,values)
                        db.commit()
                        cur.execute('SELECT * FROM fertilizerdetails where Email =%s',(email,))
                        data = cur.fetchall()
                        print(data)
                        cur.close()
                        flash('Product updated  successfully')
                        return render_template('modifyfert.html', data = data,fid = email)
                except Exception as e:
                        cur=db.cursor()
                        query="""update  fertilizerdetails set Quantity=%s,Rate=%s,imageUrl=%s, time=%s where fertilizer_ID=%s"""
                        values=(quantity,rates,fertImageURL,datetime.datetime.now(),fertid)
                        cur.execute(query,values)
                        db.commit()
                        cur.execute('SELECT * FROM fertilizerdetails where Email =%s',(email,))
                        data = cur.fetchall()
                        print(data)
                        cur.close()
                        flash('something went wrong please try it again..  ')
                        return render_template('modifyfert.html', data = data,fid = email)
                finally:
                        cur.close()

@app.route('/updatecrop/<string:id>/<string:cropid>',methods=['POST','GET'])
def updatecrop(id,cropid):
        print(id)
        try:
                
                cur = db.cursor()
                print(cropid)
                query='select   * from productdetails where cropID=%s'
                values=(cropid,)
                cur.execute(query,values)
                data = cur.fetchone()
                cur.close()
                return render_template('updatecrop.html', data = data,fid = id)
        except Exception as e:
                return str(e)
                
#modification of fertilizer
@app.route('/updatefert/<string:id>/<string:fertID>',methods=['POST','GET'])
def updatefert(id,fertID):
        print(id)
        try:
                
                cur = db.cursor()
                print(fertID)
                cur.execute('SELECT * FROM fertilizerdetails where fertilizer_ID =%s',(fertID,))
                data = cur.fetchone()
                print(data)
                cur.close()
                return render_template('updatefert.html', data = data,fid = id)
        except Exception as e:
                return str(e)    

@app.route('/displayFert/<string:type>/<string:id>',methods = ['GET','POST'])
def displayFert(type,id):
        cur = db.cursor()
        # query = 'SELECT * FROM productdetails'
        # query="SELECT * FROM productdetails"
        # query='SELECT * FROM productdetails where email= \'farmer\' '
        cur.execute('SELECT a.email,a.fertilizerName,a.Rate,a.Quantity,a.fertilizer_ID,a.imageUrl,a.time,b.phonenumber FROM fertilizerdetails as a inner join userprofile as b on a.email=b.email and a.quantity>0')
        data = cur.fetchall()
        # cur.execute('SELECT * FROM fertilizerdetails where quantity>0')
        # data = cur.fetchall()
        print(data)
        cur.close()
        print("redirecting to dispalyFert.html ")
        if(len(data)>0):
                return render_template('dispalyFert.html', data = data,fid = id)
        else:
                flash("no product to display")
                return render_template('farmer.html',id=id,type=type)


@app.route('/AddFertilizers/<string:type>/<string:email>',methods=['POST','GET'])
def AddFertilizers(type,email):
        if(request.method=='POST'):
                name=request.form["fertname"]
                quantity=request.form["quantity"]
                rates=request.form["rates"]
                #description=request.form["description"]
                cropImageURL=request.form["imageURL"]
                cur=db.cursor()
                print(quantity)
                query='INSERT INTO fertilizerdetails( Email ,fertilizerName,Rate,Quantity,imageUrl,time) values(%s,%s,%s,%s,%s,%s)'
                values=(email,name,rates,quantity,cropImageURL,datetime.datetime.now())
                cur.execute(query,values)
                db.commit()
                print("adding ferilizer")
                if(cur!=None):
                        print("!product added")
                        flash('Product Added  successfully')
                        cur.close()
                        return render_template('company.html',type=type,id=email)
                else:
                        print("not added")
                        cur.close()
                        return render_template('AddFertilizers.html',title='Addccrops',userType=type,userEmail=email)
        else:
                return render_template('AddFertilizers.html',title='Addccrops',userType=type,userEmail=email)

# @app.route('/DisplayFertilizers/<string:type>/<string:email>',methods=['POST','GET'])
# def DisplayFertilizers(type,email):
#         cur=db.cursor()
#         query='SELECT * FROM FertilizerDetails WHERE Email=%s'
#         # values=(email)
#         cur.execute('SELECT * FROM FertilizerDetails WHERE Email=%s',(email,))
#         print("showing Fertilizer")
#         if(cur!=None):
#                 datas=cur.fetchall()
#                 return render_template('displayFertilizers.html',userType=type,userEmail=email,data=datas)
#         else:
#                 print("No Items to display")
#                 return render_template('AddFertilizers.html',title='Addccrops',userType=type,userEmail=email)

@app.route("/analysis/<string:type_>/<string:consuid_>/<int:flag>",methods=['GET','POST'])
def chart(type_,consuid_,flag):
    script, div = an.chart(consuid_,flag,type)
    return render_template("chart.html", type=type_,the_div=div,the_script=script, consuid=consuid_)

@app.route("/myrequests/<string:consuid_>/<string:type_>")
def myrequests(consuid_,type_):
        try:
                cur = db.cursor()
                print(type_)
                if(type_=="Farmer"):
                        print("farmer")
                        query='SELECT id, cropName, quantity,rate,consumerid FROM requests where farmerID =%s and status=false'
                        values=(consuid_,)
                        cur.execute(query,values)
                        data = cur.fetchall()
                        cur.close()
                        print(data)
                        if(len(data)>0):
                                print("redirecting to requestscrops.html")
                                return render_template('requestscrops.html',userType = type_,fid = consuid_,data=data)
                        else:
                                flash("No Request to dispaly..")
                                return render_template('farmer.html',id=consuid_,type=type_)
                else:
                        query='SELECT  a.id, a.quantity, a.rate,a.date,a.farmerID ,b.fertilizerName FROM requestfert as a inner join fertilizerdetails as b on b.fertilizer_ID=a.fertID and  a. companyID =%s and a.status =false'
                        values=(consuid_,)
                        print("company")
                        cur.execute(query,values)
                        data = cur.fetchall()
                        #print(data[0])
                        print(data)
                        db.commit()
                        if(len(data)>0):
                                print("redirecting to requestscrops.html")
                                return render_template('requestsfertilizer.html',type = type_,fid = consuid_,data=data)
                        else:
                                flash("No Request to dispaly..")
                                return render_template('Company.html',id=consuid_,type=type_)

                        

        except Exception as e:
                 return str(e)
        finally:
                cur.close()
        return "hello"

@app.route("/acceptrequest/<string:type>/<string:consuid_>/<string:product_id>")
def acceptrequests(type,consuid_,product_id):
        print("inside accept request..")
        try:
                cur = db.cursor()
                print(cur)
                if(type=="Farmer"):
                        print("farmer")
                        query="""update requests set status= true where id=%s"""
                        values=(product_id,)
                        cur.execute(query,values)
                        db.commit()
                        query="""select consumerID from requests where id=%s"""
                        values=(product_id,)
                        cur.execute(query,values)
                        flash("Product is accepted ..information has been sent to email..")
                        data=cur.fetchone()
                        consumereID=data[0]
                        message = "Your Products is Accepted /n" 
                        #to end email to farmer
                        query="""select firstname ,phonenumber from userprofile where email=%s"""
                        values=(consuid_,)
                        cur.execute(query,values)
                        data=cur.fetchone()
                        print(data)
                        farmerinformation = "Company's email{0}, /n Company name:{1}, phonenumber {2}".format(consuid_,data[0],data[1]) 
                        print(farmerinformation)
                        message=message+str(farmerinformation)
                        print(message)
                        # to send email to farmer
                        query="""select firstname ,phonenumber from userprofile where email=%s"""
                        values=(consumereID,)
                        cur.execute(query,values)
                        data=cur.fetchone()
                        print(data)

                        farmerinformation = "Farmer's email{0}, /n farmer name:{1}, phonenumber {2}".format(consuid_,data[0],data[1]) 
                        print(farmerinformation)
                        message1=message+str(farmerinformation)
                        
                        query='SELECT id, cropName, quantity,rate,consumerid FROM requests where farmerID =%s and status=false'
                        values=(consuid_,)
                        
                        cur.execute(query,values)
                        data = cur.fetchall()
                        cur.close()
                        print(data)
                        try:
                                print("sending email..")
                                print(consuid_)
                                #message="hello"
                                print(message)
                                print(message1)
                                message=str(message)
                                s.sendmail("farmcirclesupporoficial@gmail.com",consuid_ , message)
                                s.sendmail("farmcirclesupporoficial@gmail.com",consumereID , message1)
                        except Exception as e:
                                print(e)
                                print("something wrong..")
                        finally:
                                if(len(data)>0):
                                        print("redirecting to requestscrops.html")
                                        flash("product is accepted sucessfully.... further information t will be procided through Email.. ")
                                        #print(data)
                                        return render_template('requestscrops.html',userType = type,fid = consuid_,data=data)
                                # query='SELECT * FROM requests where farmerID =%s and status=false'
                                # values=(consuid_,)
                                # cur.execute(query,values)
                                # data = cur.fetchall()
                                # db.commit()
                                else:   
                                        flash("no Product to display..")
                                        return render_template('farmer.html',id = consuid_,type="Farmer")
                else:
                        print("company")
                        query="""update requestfert set status= true where id=%s"""
                        values=(product_id,)
                        cur.execute(query,values)
                        db.commit()
                        flash("Product is accepted ..information has been sent to email..")
                        query="""select farmerID from requestfert where id=%s"""
                        values=(product_id,)
                        cur.execute(query,values)
                        data=cur.fetchone()
                        print(data)
                        consumereID=data[0]
                        message = "Your Products is Accepted" 
                        query="""select firstname ,villagename ,city, district,state,pin,phonenumber from userprofile where email=%s"""
                        values=(consuid_,)
                        cur.execute(query,values)
                        data=cur.fetchone()
                        #print(data)
                        farmerinformation = "Company's email{0}, /n Company name:{1}, villagename -{2} ,city {3},/n district {4},state {5}, pin {6}, phonenumber {7}".format(consuid_,data[0],data[1],data[2],data[3],data[4],data[5],data[6]) 
                        print(farmerinformation)
                        message=message+str(farmerinformation)
                        s.sendmail("farmcirclesupporoficial@gmail.com","deekshithvs99@gmail.com" , message)
                        # to send email to farmer
                        query="""select firstname ,villagename ,city, district,state,pin,phonenumber from userprofile where email=%s"""
                        values=(consumereID,)
                        cur.execute(query,values)
                        data=cur.fetchone()
                        print(data)
                        farmerinformation = "Farmer's email{0}, /n framer name:{1}, villagename -{2} ,city {3},/n district {4},state {5}, pin {6}, phonenumber {7}".format(consuid_,data[0],data[1],data[2],data[3],data[4],data[5],data[6]) 
                        print(farmerinformation)
                        message=message+str(farmerinformation)
                        try:
                                s.sendmail("farmcirclesupporoficial@gmail.com",consuid_ , message)
                        except:
                                print("error in sending email...")
                        finally:
                                query='SELECT  id, quantity, quantity,rate,date FROM requestfert where companyID =%s and status =false'
                                values=(consuid_,)
                                print("company")
                                cur.execute(query,values)
                                data = cur.fetchall()
                                #print(data[0])
                                print(data)
                                flash('Product Accepted  successfully')
                                db.commit()
                                print(data[0])
                                
                                query='SELECT  a.id, a.quantity, a.rate,a.date,a.farmerID ,b.fertilizerName FROM requestfert as a inner join fertilizerdetails as b on b.fertilizer_ID=a.fertID and  a. companyID =%s and a.status =false'
                                values=(consuid_,)
                                print("company")
                                cur.execute(query,values)
                                data = cur.fetchall()
                                #print(data[0])
                                print(data)
                                try:
                                        s2=setupemail()
                                        s2.sendmail("farmcirclesupporoficial@gmail.com","deekshithvs88@gmail.com" , message)
                                except Exception as e:
                                        print(e)
                                finally:
                                        db.commit()
                                        flash("product is accepted sucessfully....further information t will be procided through Email... ")
                                        if(len(data)>0):
                                                return render_template('requestsfertilizer.html',type = type,fid = consuid_,data=data)
                                        else:
                                                flash("there is no no product to dispay")
                                                return render_template('company.html',type = type,id = consuid_)

        except Exception as e:
                print(e)
                return str(e)

        return "hello"

@app.route("/deleterequest/<string:type>/<string:consuid_>/<string:product_id>")
def deleterequests(type,consuid_,product_id):
        print("dleterequests;")
        try:
                cur = db.cursor()
                print(type)
                if(type=="Farmer" or type=="farmer"):
                        print("hello")
                        query='''select consumerID from requests where id=%s'''
                        values=(product_id,)
                        cur.execute(query,values)
                        data=cur.fetchone()
                        consumer_email=data[0]
                        query="""delete from  requests where id=%s"""
                        values=(product_id,)
                        cur.execute(query,values)
                        db.commit()
                        query='SELECT id, cropName, quantity,rate FROM requests where farmerID =%s and status=false'
                        values=(consuid_,)
                        cur.execute(query,values)
                        data = cur.fetchall()
                        db.commit()
                        #print(data[0])
                       
                        flash('Deleted Request successfully')
                        print(data)
                        cur.close()
                        message="sorry,your requests has been cancelled .... "
                        s.sendmail("farmcirclesupporoficial@gmail.com", consumer_email, message) 
                        if(len(data)>0):
                                return render_template('requestsCrops.html',id = consuid_,data=data)
                        else:
                                flash("there is not product to display")
                                return render_template('farmer.html',id=consuid_,type=type)
                else:
                        query='''select FarmerID from requestfert where id=%s'''
                        values=(product_id,)
                        cur.execute(query,values)
                        data=cur.fetchone()
                        print(data)
                        farmer_email=data[0]
                        query="""delete from requestfert where id=%s"""
                        values=(product_id,)
                        cur.execute(query,values)
                        db.commit()
                        
                        message="sorry,your requests has been cancelled .... "
                        s.sendmail("farmcirclesupporoficial@gmail.com", farmer_email, message) 
                        query='SELECT  a.id, a.quantity, a.rate,a.date,a.farmerID ,b.fertilizerName FROM requestfert as a inner join fertilizerdetails as b on b.fertilizer_ID=a.fertID and  a. companyID =%s and a.status =false'
                        values=(consuid_,)
                        print("company")
                        cur.execute(query,values)
                        data = cur.fetchall()
                        #print(data[0])
                        print(data)
                        flash("Deleted Request successfully")
                        db.commit()
                        if(len(data)>0):
                                print("redirecting to requestscrops.html")
                                return render_template('requestsfertilizer.html',type = type_,fid = consuid_,data=data)
                        else:
                                flash("no request to display...")
                                return render_template('company.html',type = type,id = consuid_)

        except Exception as e:
                print(e)
                flash("Something went wrong... please try it again")
                if(type=="Farmer"):
                        return render_template('farmer.html',type = type,id = consuid_)
                else:
                        return render_template('company.html',type = type,id = consuid_)




# @app.route('/feedbaccc/<string:email>/<string:type>', methods = ['POST','GET'])
# def fedbaccc(email,type):
# 	if(request.method == "POST"):
# 		experience = request.form['experience']
# 		name = request.form['name']
# 		email = request.form['email']
# 		comments = request.form['comments']
# 		dict={"experience":experience,"Name":name,"email":email,"comments":comments}
# 		feed.insert_one(dict)
# 		return "success"
# 	else:
# 		render_template("feed.html",id=email,type=type)

# @app.route('/reviews')
# def reviews():
#         db.collection.find().sort({age:-1}).limit(1)
# 	x = feed.find({},{"Name":1, "comments":1, "email":1, "experience":1})
# 	# lis=[]
# 	# for i in x:
# 	# 	lis.append(i)
# 	# 	print(i)
# 	# # print(x)
# 	return render_template('dash.html', data = x)


# client=MongoClient()
# db=client["farmCircleDB"]
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="werock@1",
  database="farmsample"
)
def setupemail():
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls()
        s.login("farmcirclesupporoficial@gmail.com", "dharmareddy")
        return s 
client=MongoClient()
db1=client["dashrath"]
feed = db1["feed"]
# userlogin=db["userlogin"]
s=setupemail()
app.secret_key=os.urandom(12)
if __name__ == '__main__':
        
        app.run(debug=False)
   