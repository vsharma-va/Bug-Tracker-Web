export class Helper{
    static httpRequest(xmlHttpRequestVar, type, requestUrl, onReadyStateChangeFunc, dataToSend){
        xmlHttpRequestVar.open(`${type}`, `${requestUrl}`, true)
        xmlHttpRequestVar.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlHttpRequestVar.onreadystatechange = onReadyStateChangeFunc;
        xmlHttpRequestVar.send(dataToSend);
    }
}
