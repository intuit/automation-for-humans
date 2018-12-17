current_folder=$(pwd)
echo $current_folder
for file in recordings/* ; do
  if [[ -d "$file" && ! -L "$file" ]]; then
    cd $file
    convert -delay 50 -loop 0 *.png animation.gif
    cd $current_folder
  fi;
done
