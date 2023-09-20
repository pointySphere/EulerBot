import os
import discord
from discord.ext import commands
import math
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask
from sympy.solvers import solve
from sympy import Symbol, divisors
from sympy.ntheory import isprime, factorint

from asteval import Interpreter
aeval = Interpreter()

import wolframalpha
appid = os.environ['APP_ID']
app = wolframalpha.Client(appid)

app = Flask('')

@app.route('/')

def run(): app.run(host="0.0.0.0", port=8000)

def keep_alive(): 
    server = Thread(target=run) 
    server.start()

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

@client.command(name="evaluate", aliases=["eval"])
async def evaluate(ctx, expr):
    try:
        x = aeval(expr)
        await ctx.send(f"{expr} = {x}")
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name='graph')
async def graph(ctx, expr, grid=True):
    try:
        x = np.linspace(-10, 10, 1000)
        y = eval(expr)
        plt.plot(x, y)
        if grid is True:
            plt.grid()
        plt.savefig('graph.png')
        await ctx.send(f"The graph of {expr} is:")
        await ctx.send(file=discord.File('graph.png'))
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name="query", aliases=["ask"])
async def query(ctx, question):
    res = app.query(question)
    if res['@success'] == 'false':
        await ctx.send('I was unable to find an answer to your question.')
    else:
        answer = next(res.results).text
        await ctx.send(f'The answer to your question is {answer}')

@client.command(name="solve")
async def solve_(ctx, equation, symbol):
    try:
        x = Symbol(symbol)
        solution = solve(equation, x)
        await ctx.send(f"The solutions to {equation} are {solution}")
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name="isprime")
async def isprime_(ctx, n):
    try:
        if isprime(int(n)) is True:
            await ctx.send(f"{n} is prime.")
        else:
            await ctx.send(f"{n} is not prime.")
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name="primefactor", aliases=["primefactorization", "primefact"])
async def factorize(ctx, n, exp=False, symbol="^"):
    try:
        dict = factorint(n)
        if exp is False: 
            x = ' * '.join([f'{key} * {value}' for key, value in dict.items() for _ in range(value)])
            await ctx.send(f"The prime factorization of {n} is {x}")
        elif exp is True:
            if symbol == "^":
                x = ' * '.join([f'{key}^{value}' if value > 1 else f'{key}' for key, value in dict.items()])
                await ctx.send(f"The prime factorization of {n} is {x}")
            elif symbol == "**":
                x = ' * '.join([f'{key}{"**" + str(value) if value > 1 else ""}' for key, value in dict.items()])
                await ctx.send(f"The prime factorization of {n} is {x}")  
    except:
        await ctx.send("There's been an error! Modify your input.")

@client.command(name="divisors", aliases=["factor", "fact"])
async def divisors_(ctx, n):
    try:
        x = divisors(n)
        await ctx.send(f"The divisors of {n} are {x}")
    except:
        await ctx.send("There's been an error! Modify your input.")
                       
@client.command(name="goat")
async def goat(ctx):
    await ctx.send("Euler is the Greatest of All Time in mathematics.")

token = os.environ['DISCORD_BOT_SECRET']
client.run(token)
