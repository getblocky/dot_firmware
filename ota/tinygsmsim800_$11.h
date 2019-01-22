  waitResponse(85000L);
    // Query the GPRS bearer context status
    sendAT(GF("+SAPBR=2,1"));
    if (waitResponse(30000L) != 1)
      return false;

    // Attach to GPRS
    sendAT(GF("+CGATT=1"));
    if (waitResponse(60000L) != 1)
      return false;

    // TODO: wait AT+CGATT?

    // Set to multi-IP
    sendAT(GF("+CIPMUX=1"));
    if (waitResponse() != 1) {
      return false;
    }

    // Put in "quick send" mode (thus no extra "Send OK")
    sendAT(GF("+CIPQSEND=1"));
    if (waitResponse() != 1) {
      return false;
    }

    // Set to get data manually
    sendAT(GF("+CIPRXGET=1"));
    if (waitResponse() != 1) {
      return false;
    }

    // Start Task and Set APN, USER NAME, PASSWORD
    sendAT(GF("+CSTT=\""), apn, GF("\",\""), user, GF("\",\""), pwd, GF("\""));
    if (waitResponse(60000L) != 1) {
      return false;
    }

    // Bring Up Wireless Connection with GPRS or CSD
    sendAT(GF("+CIICR"));
    if (waitResponse(60000L) != 1) {
      return false;
  