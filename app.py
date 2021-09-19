from market import app
#import os
#run this command to run the app in debug mode
#docker run -p 5000:5000 -e DEBUG=1 <image-name>

if __name__=='__main__': #check if run file has executed directly
    #app.run(host='0.0.0.0',port=5000,debug=os.environ.get('DEBUG')=='1')
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=80)
#imports all the files in the right order
