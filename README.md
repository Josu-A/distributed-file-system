# Distributed File System

## Test cases

```bash
touch f1
cp /etc/passwd .
head passwd >f2
echo "Hello" >>f2
nano f2 + add some text + save the file (without exiting) + .......... + add some more text + exit nano saving the last changes to the file
rm f1
mv f2 f3
touch passwd
mkdir dir1
rmdir dir1 (assuming dir1 is empty)
```

## Events

### touch a

```
on_any_event: FileCreatedEvent(src_path='testing/a', dest_path='', event_type='created', is_directory=False, is_synthetic=False)
on_created: FileCreatedEvent(src_path='testing/a', dest_path='', event_type='created', is_directory=False, is_synthetic=False)
on_any_event: DirModifiedEvent(src_path='testing', dest_path='', event_type='modified', is_directory=True, is_synthetic=False)
on_modified: DirModifiedEvent(src_path='testing', dest_path='', event_type='modified', is_directory=True, is_synthetic=False)
on_any_event: FileOpenedEvent(src_path='testing/a', dest_path='', event_type='opened', is_directory=False, is_synthetic=False)
on_any_event: FileModifiedEvent(src_path='testing/a', dest_path='', event_type='modified', is_directory=False, is_synthetic=False)
on_modified: FileModifiedEvent(src_path='testing/a', dest_path='', event_type='modified', is_directory=False, is_synthetic=False)
on_any_event: FileClosedEvent(src_path='testing/a', dest_path='', event_type='closed', is_directory=False, is_synthetic=False)
on_closed: FileClosedEvent(src_path='testing/a', dest_path='', event_type='closed', is_directory=False, is_synthetic=False)
on_any_event: DirModifiedEvent(src_path='testing', dest_path='', event_type='modified', is_directory=True, is_synthetic=False)
on_modified: DirModifiedEvent(src_path='testing', dest_path='', event_type='modified', is_directory=True, is_synthetic=False)
```