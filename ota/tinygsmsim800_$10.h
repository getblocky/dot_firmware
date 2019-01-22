ted()) {
        return true;
      }
      delay(250);
    }
    return false;
  }

  /*
   * GPRS functions
   */
  bool gprsConnect(const char* apn, const char* user = NULL, const char* pwd = NULL) {
    gprsDisconnect();

    // Set the Bearer for the IP
    sendAT(GF("+SAPBR=3,1,\"Contype\",\"GPRS\""));  // Set the connection type to GPRS
    waitResponse();

    sendAT(GF("+SAPBR=3,1,\"APN\",\""), apn, '"');  // Set the APN
    waitResponse();

    if (user && strlen(user) > 0) {
      sendAT(GF("+SAPBR=3,1,\"USER\",\""), user, '"');  // Set the user name
      waitResponse();
    }
    if (pwd && strlen(pwd) > 0) {
      sendAT(GF("+SAPBR=3,1,\"PWD\",\""), pwd, '"');  // Set the password
      waitResponse();
    }

    // Define the PDP context
    sendAT(GF("+CGDCONT=1,\"IP\",\""), apn, '"');
    waitResponse();

    // Activate the PDP context
    sendAT(GF("+CGACT=1,1"));
    waitResponse(60000L);

    // Open the definied GPRS bearer context
    sendAT(GF("+SAPBR=1,1"));
  