
# remove old file
rm ~/load_output.csv


# first 5 minutes - extra low load
for run in {1..5}; do
    siege --quiet --log=$HOME/load_output.csv -d 100  -c 20 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

# next 2 minutes - low-medium load
for run in {1..2}; do
    siege --quiet --log=$HOME/load_output.csv -d 50  -c 20 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

# next 2 minutes - medium load
for run in {1..2}; do
    siege --quiet --log=$HOME/load_output.csv -d 10  -c 20 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

# next 1 minutes - high-medium load
for run in {1..1}; do
    siege --quiet --log=$HOME/load_output.csv -d 3  -c 20 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

# next 5 minutes - high load
for run in {1..5}; do
    siege --quiet --log=$HOME/load_output.csv -d 1  -c 20 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

# next 5 minutes - extra high load
for run in {1..5}; do
    siege --quiet --log=$HOME/load_output.csv -d 1  -c 30 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

# next 1 minutes - high-medium load
for run in {1..1}; do
    siege --quiet --log=$HOME/load_output.csv -d 3  -c 20 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

# next 2 minutes - medium load
for run in {1..2}; do
    siege --quiet --log=$HOME/load_output.csv -d 60  -c 20 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

# next 7 minutes - low load
for run in {1..7}; do
    siege --quiet --log=$HOME/load_output.csv -d 80  -c 20 -t 60s http://$(curl -s ifconfig.me/ip):32000/test
done

echo "Done! Results are in $HOME/load_output.csv"