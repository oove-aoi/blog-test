
while True:
	try:
		pay = 0
		num = float(input("請輸入用電度數:"))

		if num < 0:
			print("請輸入正數")
		elif num <= 200:
			pay = num*3.2

		elif num < 200 and num <= 300:
			pay = 200*3.2 + (num-200)*3.4

		else:
			pay = 200*3.2 + 100*3.4 + (num-300)*3.6

		print(f"你的電費是:{pay}")

	except:
		break