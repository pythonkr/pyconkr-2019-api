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
    warning
    warningKo
    warningEn
    startAt
    finishAt
    total
    remainingCount
    isSoldOut
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
          amount
          merchantUid
          impUid
          pgTid
          receiptUrl
          paidAt
        }
    }
}
'''

MY_TICKETS = '''
query getMyTickets {
  myTickets {
    isDomesticCard
    amount
    merchantUid
    receiptUrl
    paidAt
    cancelReceiptUrl
    cancelledAt
    status
    
    product{
      id
      type
      name
      nameKo
      nameEn
      desc
      descKo
      descEn
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
    options
  }
}
'''

MY_TICKET = '''
query getMyTicket($id: ID!) {
  myTicket(id: $id) {
    isDomesticCard
    amount
    merchantUid
    receiptUrl
    paidAt
    cancelReceiptUrl
    cancelledAt
    status
    
    product{
      id
      type
      name
      nameKo
      nameEn
      desc
      descKo
      descEn
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
    options
  }
}
'''

CANCEL_TICKET = '''
mutation cancelTicket($ticketId: ID!) {
    cancelTicket(ticketId:$ticketId) {
        ticket{
          id
          status
          impUid
          pgTid
          receiptUrl
          paidAt
          cancelReceiptUrl
          cancelledAt
        }
    }
}
'''
