
# Use-Case Flow Specification

## Use Case: Redeem Digital Gift Card

**Use Case ID:** UC-01
**Primary Actor:** Account Holder
**Supporting Actor:** Merchant Partner

### Preconditions

1. The Account Holder is authenticated.
2. The Account Holder has a valid digital wallet.
3. The Account Holder has sufficient universal exchange credits.
4. The requested gift card is available.
5. The system is connected to the required merchant/gift-card service.

### Postconditions

1. The required universal exchange credits are deducted from the Account Holder's wallet.
2. A unique digital voucher is generated.
3. The voucher is locked for single use.
4. The redemption transaction is recorded in the wallet ledger.
5. The Account Holder receives the digital gift card and voucher.

### Main Success Scenario

1. The Account Holder selects the desired digital gift card.
2. The system displays the gift card value and required universal exchange credits.
3. The Account Holder confirms the redemption request.
4. The system verifies that the Account Holder has sufficient exchange credits.
5. The system verifies that the selected gift card is available.
6. The system calculates the applicable redemption amount.
7. The system deducts the required exchange credits from the Account Holder's wallet.
8. The system generates a unique single-use voucher code.
9. The system applies the voucher's security/checksum information.
10. The system locks the voucher against duplicate redemption.
11. The system records the successful transaction in the ledger.
12. The system displays the digital gift card and voucher to the Account Holder.

### Alternate Flow — Insufficient Credits

**A1.** At Step 4, the system determines that the Account Holder does not have sufficient universal exchange credits.

**A2.** The system rejects the redemption request.

**A3.** The system does not deduct any credits.

**A4.** The system informs the Account Holder that the wallet balance is insufficient.

**A5.** The use case ends without generating a voucher.
