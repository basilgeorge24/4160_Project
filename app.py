from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

def deploy_resource(action):
    try:
        if action == 'aws_gcp':
            subprocess.run(['terraform', 'apply', '-auto-approve'], cwd='./modules/aws_ec2', check=True)
            subprocess.run(['terraform', 'apply', '-auto-approve'], cwd='./modules/gcp_compute', check=True)
            subprocess.run(['terraform', 'apply', '-auto-approve'], cwd='./modules/aws_rds', check=True)
            subprocess.run(['terraform', 'apply', '-auto-approve'], cwd='./modules/gcp_sql', check=True)
        else:
            subprocess.run(['terraform', 'apply', '-auto-approve'], cwd=f'./modules/{action}', check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    
def destroy_resource(action):
    try:
        if action == 'aws_gcp':
            subprocess.run(['terraform', 'destroy', '-auto-approve'], cwd='./modules/aws_ec2', check=True)
            subprocess.run(['terraform', 'destroy', '-auto-approve'], cwd='./modules/gcp_compute', check=True)
            subprocess.run(['terraform', 'destroy', '-auto-approve'], cwd='./modules/aws_rds', check=True)
            subprocess.run(['terraform', 'destroy', '-auto-approve'], cwd='./modules/gcp_sql', check=True)
        else:
            subprocess.run(['terraform', 'destroy', '-auto-approve'], cwd=f'./modules/{action}', check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_deployment_details(action):
    if action == 'aws_ec2':
        return "<span class='head-details'>AWS EC2 Instance Deployed Successfully!</span> <br><br>Created in region <span class='the-details'> US-East-2.</span> <br>Instance Type: <span class='the-details'>t2.micro</span>"
    elif action == 'gcp_compute':
        return "<span class='head-details'>GCP Compute Instance Deployed Successfully!</span> <br><br>Created in region <span class='the-details'> US-Central1. <br>Machine Type: <span class='the-details'>e2.micro</span>"
    elif action == 'aws_rds':
        return "<span class='head-details'>AWS RDS MySQL Database Deployed Successfully!</span> <span class='head-details'> A subnet group with 2 availability zones created. </span> <br><br> Instance class: <span class='the-details'>db.t3.micro</span>"
    elif action == 'gcp_sql':
        return "<span class='head-details'>GCP MySQL Database Deployed Successfully! </span>. <span class='head-details'>A subnet was created on US-Central1. </span> <br><br> Instance class: <span class='the-details'>db-f1-micro</span>"
    elif action == 'aws_gcp':
        return "<span class='head-details'>Multi-Cloud AWS-GCP deployment successful! </span>"
    else:
        return "Unknown action."


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    action = request.form['action']
    if action in ['aws_ec2', 'gcp_compute', 'aws_rds', 'gcp_sql', 'aws_gcp']:
        if deploy_resource(action):
            deployment_details = get_deployment_details(action)
            return render_template('success.html', message='Deployment Successful.', details=deployment_details)
        else:
            return render_template('error.html', message='Deployment Failed')
    else:
        return render_template('error.html', message='Invalid action')

@app.route('/destroy', methods=['POST'])
def destroy():
    action = request.form['action']
    if action in ['aws_ec2', 'gcp_compute', 'aws_rds', 'gcp_sql', 'aws_gcp']:
        if destroy_resource(action):
            return render_template('delete.html', message='Resources destroyed successfully')
        else:
            return render_template('error.html', message='Resource destruction failed')
    else:
        return render_template('error.html', message='Invalid action')

if __name__ == '__main__':
    app.run(debug=True)