#!/bin/bash
matrix() {
	local dims=${@:2}
	
	if [[ ! $dims =~ ^([1-9][0-9]*([[:space:]]+|$))+$ ]]; then
		echo "Matrix: '$dims' bad dimensions"
		return 1
	fi

	declare -gA "$1"
	local -n "mat=$1"

	mat[dims]=$dims

	for index in `get_subscripts $1`; do
		mat[$index]=0
	done
}


get_subscripts() {
	local -n "mat=$1"

	local s=""
	for i in ${mat[dims]}; do
		if [[ -z $s ]]; then
			sep=''
		else
			sep=','
		fi
		s="${s}$sep{0..$((i - 1))}"
	done

	eval echo $s
}


fill() {
	local val=$2
	for subscript in `get_subscripts $1`; do
		set $1 $subscript $val
	done
}

fillrand() {
	local start=$2
	local end=$3
	local diff=$((end - start))
	for subscript in `get_subscripts $1`; do
		set $1 $subscript $(((RANDOM % diff) + start))
	done
}

get() {
	local -n "mat=$1"

	subscript=$2
	el=${mat[$subscript]}
	if [[ -z $el ]]; then
		echo "Subscript: $subscript is bad index"
		return 1
	fi
	echo $el
}

set() {
	local -n "mat=$1"
	subscript=$2
	val=$3
	if [[ ! $val =~ ^-?[0-9]+(.[0-9]+)?$ ]]; then
		echo "Set: $val is not a number"
		return 1
	fi
	if get $1 $subscript > /dev/null; then
		mat[$subscript]=$val
		return 0
	else
		return 1
	fi
}


out() {
	local -n "mat=$1"
	for subscript in `get_subscripts $1`; do
		echo $1[$subscript]=`get $1 $subscript`
	done
}

apply() {
	local -n "left=$2"
	local -n "right=$4"
	if [[ ! ${left[dims]} == ${right[dims]} ]]; then
		echo "Apply: dimensions didn't match"
		return 1
	fi
	matrix $1 ${left[dims]}
	local -n "result=$1"
	local op=$3

	for i in `get_subscripts $1`; do
		local left_val=${left[$i]}
		local right_val=${right[$i]}
		set $1 $i `echo "$left_val $op $right_val" | bc`
	done
}

input() {
	for s in `get_subscripts $1`; do
		while true; do
			echo -n $1[$s]=
			read val
			if set $1 $s $val > /dev/null; then
				break
			fi
		done
	done
}

# matrix a 4 4
# fill a 2
# matrix b 4 4
# input b
# out b
# apply A+B a + b
# out A+B

while true; do
	echo -n "$>"
	read cmd
	eval $cmd
done
