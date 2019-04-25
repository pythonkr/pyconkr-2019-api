BUY_EARLY_BIRD_TICKET = '''
mutation BuyEarlyBirdTicket($payment: PaymentInput!) {
    buyEarlyBirdTicket(payment: $payment) {
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
