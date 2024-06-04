document.addEventListener('DOMContentLoaded', async () => {
  // Fetch publishable key and init Stripe
  const {publishableKey} = await fetch("/config").then(r => r.json())
  const stripe = Stripe(publishableKey)

  // Get the client secret
  const params = new URLSearchParams(window.location.href)
  const clientSecret = params.get('payment_intent_client_secret')

  // Get the payment intent
  const {paymentIntent} = await stripe.retrievePaymentIntent(clientSecret)
  
  // Populate the complete object for testing
  // const paymentIntentPre = document.getElementById('payment-intent')
  // paymentIntentPre.innerText = JSON.stringify(paymentIntent, null, 2)
  
  // Format the amount charged
  const formattedAmount = (paymentIntent.amount / 100).toFixed(2)
  
  // Populate the charge amount and payment intent ID's:
  document.getElementById('charge-amount').innerHTML = "Amount charged: $" +
    formattedAmount
  document.getElementById('pid').innerText = "Payment Intent ID: " + 
    paymentIntent.id
  
})
