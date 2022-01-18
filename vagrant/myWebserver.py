from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from select_all_restaurants import selectAllRestaurants
from insert_new_restaurant import insertNewRestaurant
from query_restaurant_by_id import queryRestaurantById, updateRestaurantById
from createSessionAndConnectToDB import createSessionAndConnectToDB

session = createSessionAndConnectToDB()
class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                allRestautants = selectAllRestaurants(session)

                output = ""
                output += "<html><body>"
                output +="<a href='/restaurants/new'>Make a New Restaurant</a>"
                output += '</br></br></br>'

                for restaurant in allRestautants:
                    output += restaurant.name
                    output += '</br>'
                    # Objective 2 -- Add Edit and Delete Links
                    output +="<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += '</br>'
                    output +="<a href='#'>Delete</a>"
                    output += '</br></br></br>'

                output += "</body></html>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(output)
                # print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                    <input name="restaurantName" type="text" placeholder = 'New Restaurant Name' >
                    <input type="submit" value="Create">
                </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                restaurantToEdit = queryRestaurantById(session, restaurantIDPath)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>"
                output += restaurantToEdit.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                output += "<input name ='restaurantName' type='text' placeholder = '%s' >" % restaurantToEdit.name
                output += "<input type ='submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                # return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):

            try:
                if self.path.endswith("/restaurants/new"):
                    ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('restaurantName')

                        insertNewRestaurant(session, messagecontent[0])
                    
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

                if self.path.endswith("/edit"):
                    ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('restaurantName')
                        
                        restaurantIDPath = self.path.split("/")[2]

                        updateRestaurantById(session, restaurantIDPath, messagecontent[0])
                    
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                # print output
            except:
                pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()