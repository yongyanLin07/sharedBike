from flask import Blueprint, request, render_template
from flask_login import login_required
from modules.models import Bikes, rentingRecord
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

viewDataReports = Blueprint('viewDataReports', __name__)

@viewDataReports.route('/viewDataReports',methods=['GET','POST'])
@login_required
def showReport():
    if request.method == 'POST':
        
        report_type = request.form['report']
        
        if report_type=="1":
            bikes = Bikes.query
            data = pd.read_sql(bikes.statement, bikes.session.bind)
            
            data = data.groupby(["B_Status","B_Current"])["B_Id"].count().reset_index(name="Count")
            
            status = {1:"In Use", 2:"Available", 3:"Under Repair", 4:"In Transit"}
            data = data.replace({"B_Status":status})
           
            
            fig = px.bar(data, x="B_Current", y="Count", color="B_Status", title="Number of bikes at each location",
                         labels={"B_Current":"Location", "Count":"Number of bikes", "B_Status":"Bike Status"})
            
        elif report_type=="2":
            rent_records = rentingRecord.query
            df = pd.read_sql(rent_records.statement, rent_records.session.bind)
            
            df = df.groupby(["R_Sp"])["R_Id"].count().reset_index(name="Count")
            
            # fig = px.line(df, x="R_Sp", y="Count", title="Bikes rented from different locations",
                             # labels={"R_Sp":"Location", "Count":"Number of bikes"})
            
            fig = go.Figure(data=go.Scatter(x=df["R_Sp"], y=df["Count"],
                                            line=dict(color='firebrick')))
            
            fig.update_layout(
                title="Bikes rented from different locations",
                xaxis_title="Location",
                yaxis_title="Number of bikes")
        
        elif report_type=="3":
            rent_records = rentingRecord.query
            df = pd.read_sql(rent_records.statement, rent_records.session.bind)
            
            df = df.groupby(["R_Sp"])["R_fee"].sum().reset_index(name="Count")
            
            fig = px.pie(df, values="Count", names="R_Sp", title="Revenue from each location",
                         labels={"R_Sp":"Location", "Count":"Revenue in pounds"})
                
        
        html_file = open("./templates/plot_file.html","w")
        fig.write_html(html_file)
        html_file.close()

        return render_template('plot_file.html')
    else:
        return render_template('viewDataReports.html')