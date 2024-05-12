# camstat

While watching [this video](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.youtube.com/watch%3Fv%3DyixseXhg5ZY&ved=2ahUKEwjMgZKOioiGAxX4H0QIHQJkCtMQwqsBegQIERAG&usg=AOvVaw2b3oIChZL41HrRgYjlMQ98) from Andrea Borman, one of the oldest members of the Linux community, I learned that `neofetch` will no longer be maintained, much to the world's dismay. So, I'm building an alternative with Python, while practicing software patterns on steroids.

With regards to speed, I presently don't think it's worth the headache, excess, and sacrifice of portability fetching information such as virtual memory stats by hand. Direct `ps` command invocations, for example, introduce significant overhead, as you need to fork a process for each measurement.