E FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys
core = sys.modules['Blocky.Core']

def get_bit(byteval,idx):
	return ((byteval&(1<<idx))!=0)
	
class MPR121:
	def __init__(self, port, address=0x5A):
		self.p = core.getPort( port )
		self.port = port
		self.i2c = core.machine.I2C ( scl = core.machine.Pin(self.p[0]) , sda = core.machine.Pin(self.p[1]) )
		self.address = address
		self.error = False
		self.prev = 0
		self.handler = [ [None,None] for x in range(12) ]
		self.reset()
		core.mainthread.call_soon(core.asyn.Cancellable(self.poller)())
	
	def _register8(self, register, value=None):
		if value is None:
			return self.i2c.readfrom_mem(self.address, register, 1)[0]
		self.i2c.writeto_mem(self.address, register, bytearray([value]))

	def _register16(self, register, value=None):
		if value is None:
			data = self.i2c.rea