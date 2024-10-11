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

### touch f1

```
Class 'FileCreatedEvent', SrcPath 'testing/a', DestPath '', EventType 'created', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileOpenedEvent', SrcPath 'testing/a', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/a', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/a', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### cp /etc/passwd .

```
Class 'FileCreatedEvent', SrcPath 'testing/passwd', DestPath '', EventType 'created', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileOpenedEvent', SrcPath 'testing/passwd', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/passwd', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/passwd', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### head passwd >f2

```
Class 'FileCreatedEvent', SrcPath 'testing/f2', DestPath '', EventType 'created', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileOpenedEvent', SrcPath 'testing/f2', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileOpenedEvent', SrcPath 'testing/passwd', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedNoWriteEvent', SrcPath 'testing/passwd', DestPath '', EventType 'closed_no_write', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/f2', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/f2', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### echo "Hello" >>f2

```
Class 'FileOpenedEvent', SrcPath 'testing/f2', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/f2', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/f2', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### nano f2 + add some text + save the file (without exiting) + .......... + add some more text + exit nano saving the last changes to the file

```
Class 'FileCreatedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'created', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileOpenedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileOpenedEvent', SrcPath 'testing/f2', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedNoWriteEvent', SrcPath 'testing/f2', DestPath '', EventType 'closed_no_write', IsDirectory 'False', IsSynthetic 'False'

Class 'FileDeletedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'deleted', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileCreatedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'created', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileOpenedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'

Class 'FileOpenedEvent', SrcPath 'testing/f2', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/f2', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/f2', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/f2', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'

Class 'FileDeletedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'deleted', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileCreatedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'created', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileOpenedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'

Class 'FileOpenedEvent', SrcPath 'testing/f2', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/f2', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/f2', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/f2', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
Class 'FileDeletedEvent', SrcPath 'testing/.f2.swp', DestPath '', EventType 'deleted', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### rm f1

```
Class 'FileDeletedEvent', SrcPath 'testing/f1', DestPath '', EventType 'deleted', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### mv f2 f3

```
Class 'FileMovedEvent', SrcPath 'testing/f2', DestPath 'testing/f3', EventType 'moved', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### touch passwd

```
Class 'FileOpenedEvent', SrcPath 'testing/passwd', DestPath '', EventType 'opened', IsDirectory 'False', IsSynthetic 'False'
Class 'FileModifiedEvent', SrcPath 'testing/passwd', DestPath '', EventType 'modified', IsDirectory 'False', IsSynthetic 'False'
Class 'FileClosedEvent', SrcPath 'testing/passwd', DestPath '', EventType 'closed', IsDirectory 'False', IsSynthetic 'False'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### mkdir dir1

```
Class 'DirCreatedEvent', SrcPath 'testing/dir1', DestPath '', EventType 'created', IsDirectory 'True', IsSynthetic 'True'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```

### rmdir dir1 (assuming dir1 is empty)

```
Class 'DirDeletedEvent', SrcPath 'testing/dir1', DestPath '', EventType 'deleted', IsDirectory 'True', IsSynthetic 'True'
Class 'DirModifiedEvent', SrcPath 'testing', DestPath '', EventType 'modified', IsDirectory 'True', IsSynthetic 'True'
```