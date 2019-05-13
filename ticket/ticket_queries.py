BUY_TICKET = '''
mutation BuyTicket($productId: ID!, $payment: PaymentInput!, $options: JSONString) {
    buyTicket(productId:$productId, payment: $payment, options:$options) {
        ticket{
          id
          impUid
          pgTid
          receiptUrl
          paidAt
        }
    }
}
'''
