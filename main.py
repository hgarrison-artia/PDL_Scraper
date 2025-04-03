from app import DrugMatcherApp

def main():
    state = 'LA'
    app = DrugMatcherApp(state)
    app.start()
    # Start the Tkinter event loop
    app.root.mainloop()

if __name__ == '__main__':
    main()