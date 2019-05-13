TICKET_PRODUCTS = '''
query getTicketProducts {
  conferenceProducts {
    id
    type
    name
    nameKo
    nameEn
    desc
    descKo
    descEn
    optiondescSet{
      id
      type
      key
      name
      nameKo
      nameEn
      desc
      descKo
      descEn
    }
    startAt
    finishAt
    total
    owner {
      profile {
        name
        nameKo
        nameEn
        email
        image
        avatarUrl
      }
    }
    price
    isEditablePrice
    isUniqueInType
    active
    cancelableDate
    ticketOpenAt
    ticketCloseAt
    createdAt
    updatedAt
    purchaseCount
  }
}
'''


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
