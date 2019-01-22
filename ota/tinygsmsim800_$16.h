16_t*)text;
    for (size_t i=0; i<len; i++) {
      uint8_t c = t[i] >> 8;
      if (c < 0x10) { stream.print('0'); }
      stream.print(c, HEX);
      c = t[i] & 0xFF;
      if (c < 0x10) { stream.print('0'); }
      stream.print(c, HEX);
    }
    stream.write((char)0x1A);
    stream.flush();
    return waitResponse(60000L) == 1;
  }


  /*
   * Location functions
   */

  String getGsmLocation() {
    sendAT(GF("+CIPGSMLOC=1,1"));
    if (waitResponse(10000L, GF(GSM_NL "+CIPGSMLOC:")) != 1) {
      return "";
    }
    String res = stream.readStringUntil('\n');
    waitResponse();
    res.trim();
    return res;
  }

  /*
   * Time functions
   */
  String getGSMDateTime(TinyGSMDateTimeFormat format) {
    sendAT(GF("+CCLK?"));
    if (waitResponse(2000L, GF(GSM_NL "+CCLK: \"")) != 1) {
      return "";
    }

    String res;

    switch(format) {
      case DATE_FULL:
        res = stream.readStringUntil('"');
      break;
      case DATE_TIME:
        streamSkipUntil(',');
      