#!/bin/bash

if [ $1 == "pull" ]
  then
    echo "pull from remote server to local machine"
    rsync -a --delete-during -z --progress -e "ssh -o "IdentitiesOnly=yes" -p 44051" m3304@77.234.215.138:/data/m3304/3DUnetMRI/MRI_images/data/ /home/i.selivanov/git_repo/3DUnetCNN/MRI_images/data
  else
    echo "push from local machine to remote server"
    rsync -a --delete-during -z --progress -e "ssh -o "IdentitiesOnly=yes" -p 44051" /home/i.selivanov/git_repo/3DUnetCNN/MRI_images/data/ m3304@77.234.215.138:/data/m3304/3DUnetMRI/MRI_images/data
fi