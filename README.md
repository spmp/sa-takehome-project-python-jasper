# Stripe SA take home project

## Introduction

As a part of the Stripe SA opportunity application process, Stripe have requested the completion of a take home project to examine technical aptitude and other factors, with the following instructions:

> *This is a simple e-commerce application that a customer can use to purchase a book, but it's missing the payments functionality — your goal is to integrate Stripe to get this application running! To help reduce the amount of configuration and time spent on this project, you can find boilerplate applications to use as starting points in Ruby, Javascript and Python here:*
> 
> ...
> *We provide these as a starting point, but you're welcome to use whatever language and framework you’re most comfortable with.*
> *Your output should be a simple program that allows the user to take a few actions:*
> 
> - *Select a book to purchase.*
> - *Checkout and purchase the item using Stripe Elements.*
> - *Display a confirmation of purchase to the user with the total amount of the charge and Stripe Payment Intent ID (beginning with pi_).*
> 
> *When you're done, push the project to Github or place in a zip file and return along with a document ([README.md](http://readme.md/), a Google doc, etc.) containing the following:*
> 
> - *How to build, configure and run your application.*
> - *How does the solution work? Which Stripe APIs does it use? How is your application architected?*
> - *How did you approach this problem? Which docs did you use to complete the project? What challenges did you encounter?*
> - *How you might extend this if you were building a more robust instance of the same application.*
>   - *This document will give us a chance to assess your writing abilities as well.*
>   - *We'll also extend this example later in the process if you interview in person with us, asking you to present to one of our team members and add a feature to your application. We suggest your application is structured in such a way that you’re able to run it locally and integrate other Stripe features easily later.*

## Background

This was an exciting and interesting project, which despite the challenges,  came together nicely after the dragons and other magical creatures abated. This was my first real experience in JS and HTML/CSS.

The author has experience with Python as well as cursory experience with JS, CSS, and web development. A Python approach was taken to completing this project with utilisation of documentation and examples of Stripe.

Pre-interview I had completed a Stripe integration following [Flask Stripe Tutorial | TestDriven.io](https://testdriven.io/blog/flask-stripe-tutorial/) , however, this tutorial did not utilise the *Elements* components. I opted to use the provided Python-based example as a starting point, and integrated the Stripe Elements components following the example from  [Accept a payment with the Payment Element using Python - YouTube](https://www.youtube.com/watch?v=tCSbCk5j3Tk) .

## Build, configure, and run

This Python project has been developed and tested in a 'GNU/Linux' (Ubuntu 24.04) environment only, using Python 3.123. 

The document assumes a compatible version of Python and a Bash (or similar) shell are available to perform the prerequisite and run steps. 

**Warn:** Steps have been taken to correct EOL characters for use in a MS Windows environment; this has not been tested in MS Windows, your mileage may vary. 

**Warn:** The `requirements.txt` file does not contain version information as outdated Python-Stripe libraries will be incompatible with the running Stripe API's.

### Prerequisites

The Python application will be run from a _virtual environment_ as is best practice:

1. Clone or download the project into a desired location:
   
   ```bash
   git clone https://github.com/spmp/sa-takehome-project-python-jasper.git
   ```

2. Open a (Bash) shell in the directory containing this project

3. Create and activate the Python virtual environment:
   
   ```bash
   python3 -m venv venv && source venv/bin/activate
   ```

4. Install the requirements:
   
   ```bash
   pip install -r requirements.txt
   ```

5. Add your Stripe *Secret* and *Publishable* key to the file `sample.env`  and save as `.env`. The keys are available on your Stripe dashboard at: [Stripe Dashboard](https://dashboard.stripe.com/apikeys)

### Run

The application is run via a Bash or similar shell session from the root directory of this project as:

```bash
source venv/bin/activate
flask --app app.py run
```

The application will launch a web-server on the local host at an available port. Please copy and paste the `Running on` address into a browser window to start playing with the application. For example, in GNU/Linux the initial load output is:

```bash
$ flask --app app.py run
 * Serving Flask app 'app.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

You would open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

In the case where the default port is in use, please change to a free port. For example:

```bash
flask --app app.py run --port 4242 
```

Enjoy 👌🤗

## Discussion

### Architecture and other considerations

The project utilises Stripe Elements to provide payment as requested in the brief of the project. An approach used in a previous example utilised items managed within Stripe which is a much simpler approach for a small number of items.

My traditional data engineering background had me searching for ways to create an offline 'test driven' solution; unfortunately this is not possible given the live nature of the Stripe API's.

I opted to keep the project as vanilla as possible, with no database of items, instead choosing to stick to the hard-coded elements despite obvious scaling issues.

A security concern was uncovered in providing the purchase amount as part of a requesting URL to get the *client secret* as this is susceptible to modification by a malicious user. A more secure approach is to provide an endpoint which returns the the client secret utilising server-side state to determine the purchase amount. In this example the state is provided simply via a global variable.

### Challenges

Being very new to web development I ran foul of many small issues which have taught me a lot; in hindsight all is simple. At times I was convinced the existence of a cat in the room may have been the problem. As it turns out it was all operator-error.

I approached the problem via iterative problem solving. Make the simplest form work, and move out from there. With big changes that broke I used bisection to find the issue.

I experimented for a while with utilising the `stripe-mock` project so as to provide a solution which did not require any external account or setup. Unfortunately this approach does not work as the package is not intended to provide an offline test environment for Stripe development.

### Extensions

For the sample project to work in the real world it would need to at least address the following:

1. The ability to manage more than one item in a cart before *checkout*.

2. Items stored centrally, either in a database or database like file.

3. Handle multiple clients and manage their state.
