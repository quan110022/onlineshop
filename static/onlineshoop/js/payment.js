// Create a Stripe client.
// Note: this merchant has been set up for demo purposes.
var stripe = Stripe('pk_test_6pRNASCoBOKtIshFeQd4XMUh');

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    padding: '10px 12px',
    color: '#32325d',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    },
  },
  invalid: {
    color: '#fa755a',
  }
};

// Create an instance of the idealBank Element.
var idealBank = elements.create('idealBank', {style: style});

// Add an instance of the idealBank Element into the `ideal-bank-element` <div>.
idealBank.mount('#ideal-bank-element');
var errorMessage = document.getElementById('error-message');

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  showLoading();

  var sourceData = {
    type: 'ideal',
    amount: 1099,
    currency: 'eur',
    owner: {
      name: document.querySelector('input[name="name"]').value,
    },
    // Specify the URL to which the customer should be redirected
    // after paying.
    redirect: {
      return_url: 'https://shop.example.com/crtA6B28E1',
    },
  };

  // Call `stripe.createSource` with the idealBank Element and additional options.
  stripe.createSource(idealBank, sourceData).then(function(result) {
    if (result.error) {
      // Inform the customer that there was an error.
      errorMessage.textContent = result.error.message;
      errorMessage.classList.add('visible');
      stopLoading();
    } else {
      // Redirect the customer to the authorization URL.
      errorMessage.classList.remove('visible');
      stripeSourceHandler(result.source);
    }
  });
});