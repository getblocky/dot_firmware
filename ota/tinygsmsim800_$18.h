ssl && rsp != 1) {
      return false;
    }
#endif
    sendAT(GF("+CIPSTART="), mux, ',', GF("\"TCP"), GF("\",\""), host, GF("\","), port);
    rsp = waitResponse(75000L,
                       GF("CONNECT OK" GSM_NL),
                       GF("CONNECT FAIL" GSM_NL),
                       GF("ALREADY CONNECT" GSM_NL),
                       GF("ERROR" GSM_NL),
                       GF("CLOSE OK" GSM_NL)   // Happens when HTTPS handshake fails
                      );
    return (1 == rsp);
  }

  int modemSend(const void* buff, size_t len, uint8_t mux) {
    sendAT(GF("+CIPSEND="), mux, ',', len);
    if (waitResponse(GF(">")) != 1) {
      return 0;
    }
    stream.write((uint8_t*)buff, len);
    stream.flush();
    if (waitResponse(GF(GSM_NL "DATA ACCEPT:")) != 1) {
      return 0;
    }
    streamSkipUntil(','); // Skip mux
    return stream.readStringUntil('\n').toInt();
  }

  size_t modemRead(size_t size, uint8_t mux) {
#ifdef TINY_GSM_USE_HEX
    sendAT(GF("+CIPRXGET=3,"), 