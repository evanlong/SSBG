My end goal is to make a tool that allows developers to describe their REST API in some sort of markup and then generate libraries that communicate with the server. The tool would generate language specific libraries that abstract away communication with the server. I also hope to provide someway to map between the XML/JSON that the server returns and objects that are defined by the user. I think the real benefit of this will be that developers won't have to write a new library for each language they wish to support on the client side. It seems like the community is responsible for building libraries for the different languages but it would be nice if it were a little more streamlined. 

This snippet of code is simple but just the start. It just allows a way to use a python decorator to define the services interface and then the user can use the decorated function to actually communicate with the server. At the bottom I have already defined a couple of functions using the Twitter and Pownce APIs.

    :::python
    import urllib
    import re
     
    class WebApiOpener(urllib.FancyURLopener):
        '''
        Provides a way for HTTP Basic authentication to take place without
        prompting the user for a username and password like FancyURLopener
        would.
        '''
        def __init__(self, username, password):
            urllib.FancyURLopener.__init__(self,{})
            self.username = username
            self.password = password
            
        def prompt_user_passwd(self, host, realm):
            return (self.username,self.password)
     
    def webcall(**apiargs):
        '''
        Decorator that is used to create a python function that communicates with
        a RESTful web service. The function it generates will be able to to do HTTP
        basic authorization. The generated function only accepts a keyword 
        arguments. The following are reserved arguments:
            auth_username, string optional, only needed if web service needs 
            basic HTTP auth
            auth_password, string optional, only needed if web service needs
            basic HTTP auth
        All other arguments will be used to first replace variables within the url
        and the remaining arguments will be passed as part of the parameter string.
        Take a look at the documentation below and the examples to get an idea of 
        how to define variables within the url string. 
        
        webcall Arguments: apiargs, keyword list of arguments
            apiargs['url'], string, The url of the web service. Specify variables 
            for within the url like this: {var_name=default_value} or {var_name}. 
            These will be filled in when the user actually calls the decorated 
            function.
            
            apiargs['method'], string optional, Defaults to GET if not defined. If
            it is defined to something besides GET it will use POST. 
            
        Example:
            #Here we define a call to twitter:
            @webcall(url='http://twitter.com/statuses/friends_timeline.{format=json}', method='GET')
            def friends_timeline(): pass
            
            #returns a a json string for this specific twitter call
            friends_timeline(auth_username='bob', auth_password='password')
            
            #Looking at the twitter documentation we see that this takes in other
            #parameters like since, since_id, count, page.
            #we will also get the RSS formatted response and limit it to two
            friends_timeline(auth_username='bob', auth_password='password', count=2, format='rss')
        '''
        method = apiargs.get('method','GET')
        patter_obj = re.compile("\{[^\}]+\}")
        def dec(fn):
            def convert_url(url, replace_dict):
                for match in patter_obj.finditer(url):
                    #figure if the key is in the dict if not and there is
                    #no default value then don't replace and continue on
                    tmp = match.group()[1:-1]
                    pair = tmp.split('=')
                    #if there is a default value and key not in dict use default
                    if len(pair) > 1 and not replace_dict.has_key(pair[0]):
                        url = url.replace(match.group(), pair[1])
                    elif len(pair) > 0 and replace_dict.has_key(pair[0]):
                        url = url.replace(match.group(), replace_dict[pair[0]])
                        #this allow for a {key} to only be user once but this could
                        #be changed in the future
                        del(replace_dict[pair[0]])
                return url
            
            def new(**kwargs):
                '''
                auth_username and auth_password are reserved
                '''
                opener = WebApiOpener(kwargs.get('auth_username',''),
                    kwargs.get('auth_password',''))
                if kwargs.has_key('auth_username'): del(kwargs['auth_username'])
                if kwargs.has_key('auth_password'): del(kwargs['auth_password'])
                url = convert_url(apiargs['url'], kwargs)
                params = urllib.urlencode(kwargs)
                if method == 'GET':
                    stream = opener.open(url + "?" + params)
                else:
                    stream = opener.open(url, params)
                response = stream.read()
                return response
            return new
        return dec
     
    '''
    A set of example functions from pownce and twitter
    '''
     
    @webcall(url='http://twitter.com/statuses/public_timeline.{format=json}')
    def public_timeline(): pass
     
    @webcall(url='http://twitter.com/statuses/friends_timeline.{format=json}', method='GET')
    def friends_timeline(): pass
     
    @webcall(url='http://twitter.com/statuses/user_timeline.{format=json}', method='GET')
    def user_timeline(): pass
     
    @webcall(url='http://api.pownce.com/2.0/note_lists/{username}.{format=json}', method='GET')
    def pownce_note_list(): pass
     
    @webcall(url='http://api.pownce.com/2.0/send/link.{format=json}', method='POST')
    def pownce_send_link(): pass

