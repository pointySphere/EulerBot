import os
import discord
from discord.ext import commands
import math
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask
from threading import Thread
from sympy.solvers import solve
from sympy import Symbol, divisors
from sympy.ntheory import isprime, factorint

from asteval import Interpreter
aeval = Interpreter()

import wolframalpha
client_id = os.environ['CLIENT_ID']
client = wolframalpha.Client(client_id)

theport = os.environ['PORT']

app = Flask(__name__)

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=theport)

def keep_alive():
  server = Thread(target=run)
  server.start()

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("I'm in")
    print(bot.user)

@bot.command(name="evaluate", aliases=["eval"])
async def evaluate(ctx, expr):
    try:
        x = aeval(expr)
        await ctx.send(f"{expr} = {x}")
    except:
        await ctx.send("There's been an error! Modify your input.")

@bot.command(name='graph')
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

@bot.command(name="query", aliases=["ask"])
async def query(ctx, question):
    res = client.query(question)
    if res['@success'] == 'false':
        await ctx.send('I was unable to find an answer to your question.')
    else:
        answer = next(res.results).text
        await ctx.send(f'The answer to your question is {answer}')

@bot.command(name="solve")
async def solve_(ctx, equation, symbol):
    try:
        x = Symbol(symbol)
        solution = solve(equation, x)
        await ctx.send(f"The solutions to {equation} are {solution}")
    except:
        await ctx.send("There's been an error! Modify your input.")

@bot.command(name="isprime")
async def isprime_(ctx, n):
    try:
        if isprime(int(n)) is True:
            await ctx.send(f"{n} is prime.")
        else:
            await ctx.send(f"{n} is not prime.")
    except:
        await ctx.send("There's been an error! Modify your input.")

@bot.command(name="primefactor", aliases=["primefactorization", "primefact"])
async def factorize(ctx, n, exp=False):
    try:
        dict = factorint(int(n))
        if exp is False: 
            x = ' * '.join([' * '.join([str(key)] * value) for key, value in dict.items()])
            await ctx.send(f"The prime factorization of {n} is {x}")
        else:
            x = ' * '.join([f'{key}^{value}' if value > 1 else f'{key}' for key, value in dict.items()])
            await ctx.send(f"The prime factorization of {n} is {x}")
    except:
        await ctx.send("There's been an error! Modify your input.")

@bot.command(name="divisors", aliases=["factor", "fact"])
async def divisors_(ctx, n):
    try:
        x = divisors(int(n))
        await ctx.send(f"The divisors of {n} are {x}")
    except:
        await ctx.send("There's been an error! Modify your input.")
                       
@bot.command(name="goat")
async def goat(ctx):
    await ctx.send("Euler is the Greatest of All Time in mathematics.")

token = os.environ['DISCORD_BOT_SECRET']
bot.run(token)
