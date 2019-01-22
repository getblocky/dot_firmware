  }

    // Get Local IP Address, only assigned after connection
    sendAT(GF("+CIFSR;E0"));
    if (waitResponse(10000L) != 1) {
      return false;
    }

    // Configure Domain Name Server (DNS)
    sendAT(GF("+CDNSCFG=\"8.8.8.8\",\"8.8.4.4\""));
    if (waitResponse() != 1) {
      return false;
    }

    return true;
  }

  bool gprsDisconnect() {
    // Shut the TCP/IP connection
    sendAT(GF("+CIPSHUT"));
    if (waitResponse(60000L) != 1)
      return false;

    sendAT(GF("+CGATT=0"));  // Deactivate the bearer context
    if (waitResponse(60000L) != 1)
      return false;

    return true;
  }

  bool isGprsConnected() {
    sendAT(GF("+CGATT?"));
    if (waitResponse(GF(GSM_NL "+CGATT:")) != 1) {
      return false;
    }
    int res = stream.readStringUntil('\n').toInt();
    waitResponse();
    if (res != 1)
      return false;

    sendAT(GF("+CIFSR;E0")); // Another option is to use AT+CGPADDR=1
    if (waitResponse() != 1)
      return false;

    return true;
  }

