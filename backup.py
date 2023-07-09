
# 新线程执行的代码:
def blink_loop(*args, **kwargs):
	try:
		delay_ms = 500
		while True:
			GPIO.output(args, GPIO.HIGH)
			time.sleep(delay_ms/1000)
			GPIO.output(args, GPIO.LOW)
			time.sleep(delay_ms/1000)

	except:
		print("except")
		GPIO.output(args, GPIO.HIGH)
		GPIO.cleanup()


#	led    = LED.LED(GPIO_LED_RED)

#		led_blink = threading.Thread(target=blink_loop, name='led_blink', args=(GPIO_LED_RED,))
#		led_blink.start()
