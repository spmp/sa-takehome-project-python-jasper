document.addEventListener('DOMContentLoaded', async () => {
  // Fetch publishable key and init Stripe
  const {publishableKey} = await fetch("/config").then(r => r.json())
  const stripe = Stripe(publishableKey)

  // Fetch client secret and iniatilise elements
  const {clientSecret}  = await fetch("/create-payment-intent", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(r => r.json())

  const elements = stripe.elements({clientSecret})
  const paymentElement = elements.create('payment')
  paymentElement.mount('#payment-element')
  
  // Prevent the default behaviour and instead route to a sucess page on success
  // NOTE: The error handling has not been well tested!
  const form = document.getElementById('payment-form')
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const {error} = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: location.protocol.concat("//")
          .concat(window.location.host).concat("/")
          .concat("success")
      }
    })
    if(error) {
      const messages = document.getElementById('error-messages')
      messages.innerText - error.message;
    }
  })
})
