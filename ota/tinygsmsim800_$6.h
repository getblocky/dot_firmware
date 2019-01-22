endAT(GF("&W"));       // Write configuration
    return waitResponse() == 1;
  }

  String getModemInfo() {
    sendAT(GF("I"));
    String res;
    if (waitResponse(1000L, res) != 1) {
      return "";
    }
    res.replace(GSM_NL "OK" GSM_NL, "");
    res.replace(GSM_NL, " ");
    res.trim();
    return res;
  }

  bool hasSSL() {
#if defined(TINY_GSM_MODEM_SIM900)
    return false;
#else
    sendAT(GF("+CIPSSL=?"));
    if (waitResponse(GF(GSM_NL "+CIPSSL:")) != 1) {
      return false;
    }
    return waitResponse() == 1;
#endif
  }

  /*
   * Power functions
   */

  bool restart() {
    if (!testAT()) {
      return false;
    }
    //Enable Local Time Stamp for getting network time
    // TODO: Find a better place for this
    sendAT(GF("+CLTS=1"));
    if (waitResponse(10000L) != 1) {
      return false;
    }
    sendAT(GF("&W"));
    waitResponse();
    sendAT(GF("+CFUN=0"));
    if (waitResponse(10000L) != 1) {
      return false;
    }
    sendAT(GF("+CFUN=1,1"));
    if 