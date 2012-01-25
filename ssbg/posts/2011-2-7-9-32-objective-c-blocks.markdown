Objective-C features anonymous functions via what they call blocks. I was a little fuzzy on the memory management rules of blocks at first. The basic rules are: the block structure is stack allocated and blocks retain Objective-C objects they reference until the block is deallocated. In order to keep the block around beyond the lifetime of a stack frame the block must be copied to the heap All of the objects directly referenced within the block will be retained. When the block is released those objects will also be released. Keep in mind the retained objects may have weak references to other objects that may end up getting freed before one would expect. For example, an objects delegate is typically not retained. A simple mistake would be to perform an asynchronous action which causes a view to update but has the possibility of the delegate being released before that action has the opportunity to complete With the Flickr app I spoke of [previously]({{posts_path}}2011-1-31-8-28-the-great-uitableview-race.html) I messed up on both rules. First, my block referenced `tableView` whose delegate was the view controller. With the code below it will likely fail if the user backs away before all the thumbnails finish loading.

    :::objective-c
    - (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
        
        ...code to dequeue and setup a UITableViewCell removed...
     
        //retrieve our Core Data representation of the photo
        Photo* photo = [Photo photoWithFlickrData:pictObj inManagedObjectContext:context];
        if (photo.thumbnail) {
            cell.imageView.image = [UIImage imageWithData:photo.thumbnail];
        }
        else {
            //Photo objects uses Grand Central Dispatch to make a request to 
            //Flickr servers for photo downloads.
            [photo thumbnailWithBlock:^(NSData* image) {
                cell.imageView.image = [UIImage imageWithData:image];
                [tableView reloadRowsAtIndexPaths:[NSArray arrayWithObject:indexPath] withRowAnimation:UITableViewRowAnimationNone];
            }];
        }
     
        return cell;
    }

Once the user backs away from the table’s view controller it will be released. It is possible the queue will still be downloading thumbnails. Once a thumbnail is downloaded the block passed to thumbnailWithBlock will be called and attempt to update the table only to have the program crash. Instead of sending the reload message to `tableView` I send the reload message to `self.tableView`. In this case self is the view controller for the table view and since it is now reference in the block it will be retained for later use. After using Grand Central Dispatch (GCD) to perform the image fetching I wanted to see how it could be done with `NSURLConnection`. `NSURLConnection` handles all of the networking on a separate thread. It notifies the UI thread via various delegate methods of the download progress. I simply changed the `thumbnailWithBlock` on the Photo object to use `NSURLConnection` and store a pointer to the block object for use later. When the download finished I called the block with the downloaded data but the program crashed. The reason was I had failed to copy the block to the heap and was getting the `EXC_BAD_ACCESS` error. The fix was to send a copy message to the block and be sure to release it after using it with the downloaded data. Once I figured that all out I wondered how GCD handled blocks. It must copy them or else it would be getting `EXC_BAD_ACCESS` errors. Me being curious I went and looked and sure enough they [copy](http://libdispatch.macosforge.org/trac/browser/trunk/src/queue.c#L692) the blocks before using them.
