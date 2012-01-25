For the iTunes U course on iOS programming I followed along with the homework assignments. The last assignment was a Flickr app that shows photos at popular geotagged locations. I had an issue with UITableViewCell reuse and background threads populating the thumbnail image that I thought was worth sharing.   On iOS in order to improve performance some of the different libraries like UIKit and MapKit have the ability to reuse UI elements once they are no longer on screen. When reuse occurs it is up to the developer to provide new data for the UI element.  My problem was that two or more asynchronous operations could change the same table cell. One solution would be to stop reusing table cells but that is not ideal. As long as I can identify which image should be shown in the cell at a given time I can make sure the correct asynchronous operation updates the cell. Since UITableViewCell derives from UIView it has the tag property which is a NSInteger. The UITableView represents an array of data from Flickr. Before making the asynchronous call I set the cell’s tag to the index in that array it currently represents. Then in the callback function I only update the cell if its tag matches the index for which the asynchronous call was made.   Without this change in place it is possible to scroll through the list rapidly and see the thumbnail change two or three times for a cell while the remaining thumbnail downloads finish. But the last update could be the wrong thumbnail. The code itself is simple and can be found here: 

    :::objective-c
    - (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
        static NSString *CellIdentifier = @"Cell";
        
        UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
        if (cell == nil) {
            cell = [[[UITableViewCell alloc] initWithStyle:UITableViewCellStyleSubtitle reuseIdentifier:CellIdentifier] autorelease];
        }
     
        NSDictionary* pictObj = [self.pictures objectAtIndex:indexPath.row];
        NSString* title = [pictObj objectForKey:@"title"];
        title = [title length] == 0 ? @"(no title)" : title;
        cell.textLabel.text = title;
        cell.detailTextLabel.text = [[pictObj objectForKey:@"description"] objectForKey:@"_content"];
        cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator;
     
        //identify which image the cell should be displaying right now
        cell.tag = indexPath.row;
     
        Photo* photo = [Photo photoWithFlickrData:pictObj inManagedObjectContext:context];
        if (photo.thumbnail) {
            cell.imageView.image = [UIImage imageWithData:photo.thumbnail];
        }
        else {
            cell.imageView.image = nil;
            [photo thumbnailWithBlock:^(UIImage* image) {
                //check to make sure the image should be updated
                if (cell.tag == indexPath.row) {
                    cell.imageView.image = image;
                    [self.tableView reloadRowsAtIndexPaths:[NSArray arrayWithObject:indexPath] withRowAnimation:UITableViewRowAnimationNone];
                }
            }];
        }
     
        return cell;
    }
