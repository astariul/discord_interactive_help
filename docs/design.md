# General Design

This page just describes the requirements for this package, the high-level idea of what it's trying to achieve.

## What we want

We want a more user-friendly way to interact with Discord bot than the basic command line.

In order to do this, we follow the already existing idea of creating a extra-simplified UI with the reactions of Discord, as shown in the  [introduction](index.md#introduction).

**We want to completely erase the use of command lines.**

In order to do this, reactions are not enough. We also need to retrieve the input of the user, display different page depending on the user and its input, etc...

## Requirements

### Basics

Let's call the core requirement a **Help system**. The basic idea is that we need several pages, and a way to allow the user to navigate through the pages.

We are going to use a tree, where each node represent a page of the help, that the user can visualize.

Each page is linked to several child pages, and the user should be able to choose which page to display next.

![](https://user-images.githubusercontent.com/22237185/58003999-12220c00-7b1d-11e9-921f-f908687144e3.png)

In this example, the user start from Page 1, and depending on his choice, he can go to Page 2 or Page 3.

### Link back to parents

To make this help system easier to naviguate, we want to add some path back to parents, so the user can as well choose to come back one step before.

![](https://user-images.githubusercontent.com/22237185/58006319-c4100700-7b22-11e9-979d-c802f243ddf2.png)

---

We also add the idea of "root", so the user can come back to the beginning easily.

![](https://user-images.githubusercontent.com/22237185/58006335-cd996f00-7b22-11e9-919c-3c2100619e42.png)

### Dynamic content with callbacks

Our system so far is cool, but our system is static.

We want to make it more dynamic. For example, let's say we want to display a page with the user's name and role in it.
We are gonna need callbacks !

![](https://user-images.githubusercontent.com/22237185/58009134-bf4e5180-7b28-11e9-9fd4-f5652e37fa79.png)

As we can see, callbacks need to be called "in-between" 2 pages, allowing the callback to modify the content of the next page dynamically.

### More input from the user !

Our system allow the user to navigate through pages using choices (Page 2 or Page 3 for example). But to add better content, we need to get more than a choice : we need inputs.

A good example is a database search. Let's say we want to make a page where the user can search the name of a guild, and the page displayed will show information about that guild.

So we need a special link between pages that instead of waiting for the user's reaction, will wait for the user's input.

![](https://user-images.githubusercontent.com/22237185/58074754-f849fd00-7be0-11e9-91a1-3ee04f373ea3.png)

Like other links, after the user input something, callbacks can be called to change the next page dynamically.

### Multiple-choice links

Changing the next page dynamically is ok if we simply need to change **one** page. But it's awkward to do in the case where we want to change the _path_ of the tree.

To make the architecture more flexible, we associate to each link several pages, and callbacks can choose which page will be displayed (based on some information stored in database for example).

![](https://user-images.githubusercontent.com/22237185/58142649-f3d62080-7c82-11e9-922e-2f7c0584c648.png)

In this example, user will choose between page 2 and page 3, and the callback will either redirect him to page 2-1 or page 2-2, which are different and lead to different part of the help system.

### The first page is like any other page

The first page of the help should be like any other page : possibility to run callbacks before displaying it, possibility to choose between several first page depending on the callbacks.

![](https://user-images.githubusercontent.com/22237185/58143503-ff771680-7c85-11e9-87a5-dc3d25d95f54.png)

## Implementation

About the implementation, nothing complicated.

We just need 2 objects to represent the tree : `Page` and `Link`.

And we need one object to take care of all the technical stuff, roaming the tree, waiting for user's input, displaying page, etc... : `Help`.

---

About the `Link` objects, we are also going to make several subclasses :

* `ReactLink` : A `Link` where the user have to react (through Discord reactions).
* `MsgLink` : A `Link` where the user have to input a message.
* `RootLink` : A special `Link`, used at the beginning of the tree.
