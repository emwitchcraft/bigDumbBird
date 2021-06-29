# bigDumbBird
WIP

Use python to write ulps for eagle instead of the trash built in language, but still launch them from within eagle via generated ulp.

Change first line of 'ulpGenerator.py' to your '/eagle/ulps/' directory.

Just drop your python file onto 'ulpGenerator.py' and it will generate the ulp needed to call your py script and place that ulp in your eagle ulp folder.

A prompt will show up when you do this asking if it should execute as a ulp or a scr.

Executing as a ulp is largely for py scripts that read file data and produce an output.

Executing as a scr is for when you want to alter the file (use the ScriptWriter class in bigDumbBird.py).

You could change the file directly and save it from your py script and execute as a ulp, but then you won't be able to ctr+z your way out of whatever the py script did.

Using the ScriptWriter class will create a scr file that will be returned by the calling ulp and executed by eagle as editor commands.


