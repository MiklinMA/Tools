#!/usr/bin/env groovy
/* 
 * 2018
 * Mike Miklin <MiklinMA@gmail.com>
 *
 * Simple redirect from HTTP to HTTPs
 * without Apache or Nginx
 *
 */
import com.sun.net.httpserver.*

def port = 8888
def server = HttpServer.create(new InetSocketAddress(port), 0)

server.createContext("/", 
    { HttpExchange exchange ->	
        def url = [
            "https://",
            exchange.requestHeaders.getFirst("Host"),
            exchange.requestURI.path
        ].join('')

        println(exchange.requestMethod + " - " + url)
        exchange.responseHeaders.set("Location", url)
        exchange.sendResponseHeaders(301, 0)
    } as HttpHandler
)
server.start()
println "Server started"

