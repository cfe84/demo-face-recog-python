import sys
from processPicture import process_picture

#urlin = "https://demobatch.blob.core.windows.net/people/Justin-Bieber-Selena-Gomez-Struggling-559x395.jpg?st=2018-03-22T14%3A49%3A00Z&se=2018-03-23T14%3A49%3A00Z&sp=rl&sv=2017-04-17&sr=b&sig=cZFbTWs1Cgb5jaC509DG7M6jLeEvNcSR8qZ1P4PI79U%3D"
#urlout = "https://demobatch.blob.core.windows.net/output/bieber.out.jpg?st=2018-03-22T07%3A49%3A00Z&se=2018-03-23T07%3A49%3A00Z&sp=rwl&sv=2017-04-17&sr=c&sig=p1LR7Q%2FX%2FPXp%2FSxaCARcfq0VNzVVdfq3UXUXZBzWdN0%3D"

urlin = sys.argv[1]
urlout = sys.argv[2]

print("Transforming " + urlin + " to " + urlout)
process_picture(urlin, urlout)
print("Done")